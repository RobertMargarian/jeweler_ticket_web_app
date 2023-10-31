from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render, redirect
from django.db.models import Sum
from django.views import generic
from .models import Client, Plan, Owner
from django.views.generic.edit import FormView
from .forms import ClientCreateForm, CustomUserCreationForm, CompanyCreateForm, PaginationForm
from django.db.models import Case, When, DecimalField
from django.db.models import Q
from populate_location.zip_code_data import parse_zipcode_data
from django.http import JsonResponse

class Client_AutoComplete(LoginRequiredMixin, generic.View):
    def get(self, request):
        client_search_query = request.GET.get('term', '')
        clients = Client.objects.all()
        for term in client_search_query.split():
            clients = clients.filter( Q(client_first_name__icontains = term) | \
                                        Q(client_last_name__icontains = term) | \
                                        Q(client_email__icontains = term) | \
                                        Q(client_phone__icontains = term) \
                                    )     
        clients = clients.filter(deleted_flag=False)   
        results = [client.client_first_name+' '+client.client_last_name+' | '+client.client_email + ' | '+client.client_phone for client in clients]
        print(results)
        return JsonResponse(results, safe=False)


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = "customers/client_list.html"
    context_object_name = "client_list"

    def get_paginate_by(self, queryset):
        return self.request.user.pref_clients_per_page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form with the user's preference

        page_size = self.request.GET.get('page_size', self.request.user.pref_clients_per_page)
        context['clients_per_page'] = page_size
        context['pagination_form_clients'] = \
            PaginationForm(initial={'page_size': page_size})
        return context


    def get_queryset(self):
        user = self.request.user
        client_details = self.request.GET.get('client_details', None)

        if user.is_owner or user.is_employee: 
            queryset = Client.objects \
                .filter(company=user.company) \
                .filter(company=self.request.user.company) \
                .filter(deleted_flag=False) \
                .order_by('-created_at') \
                .filter(company=self.request.user.company)
            
            if client_details:
                for term in client_details.replace('|', '').split():
                    queryset = queryset.filter( Q(client_first_name__icontains = term) | \
                                                Q(client_last_name__icontains = term) | \
                                                Q(client_email__icontains = term) | \
                                                Q(client_phone__icontains = term) \
                                            )
            
            queryset = queryset.annotate(
                total_spent_column=Sum(
                    Case(
                        When(order__work_order_status__in=['Completed', 'In Progress'],
                            order__deleted_flag=False,
                            then='order__quoted_price'),
                            default=0,
                            output_field=DecimalField()
                    )
                )
            )
        else:
            return KeyError("User does not have permission to view clients")
        return queryset
    
    def get(self, request, *args, **kwargs):
        # Check if page_size is being updated
        if 'page_size' in request.GET:
            try:
                page_size = request.GET.get('page_size')
                # Update the user's preference in the model
                request.user.pref_clients_per_page = page_size
                request.user.save()
            except ValueError:
                pass
        return super().get(request, *args, **kwargs)


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    second_form_class = CompanyCreateForm
    success_url = '/login/'  # Redirect URL after successful form submission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['second_form'] = self.second_form_class()
        context['form_errors'] = self.get_form().errors
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        second_form = self.second_form_class(request.POST)

        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form, second_form)
        else:
            return self.form_invalid(form, second_form)
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            zip_code = request.GET.get('zip_code')
            zip_code_data = parse_zipcode_data(settings.ZIPCODE_DATA_FILE)

            if zip_code in zip_code_data:
                city = zip_code_data[zip_code]['city']
                state = zip_code_data[zip_code]['state']
                data = {
                    'city': city,
                    'state': state
                }
            else:
                data = {
                    'city': '',
                    'state': ''
                }
            return JsonResponse(data)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, second_form):
        company = second_form.save(commit=False)

        if Plan.objects.filter(plan_name = "Basic").exists():
            company.company_current_plan = Plan.objects.get(plan_name = "Basic")
        else:
            Plan.objects.create(plan_name = "Basic",
                                plan_frequency = "Monthly",
                                plan_price = 200, 
                                plan_currency = "USD",
                                plan_trial_period = "No",
                                )
            company.company_current_plan = Plan.objects.get(plan_name = "Basic")
        
        company.company_subscription_status = "Active"
        company.company_country = "United States"

        zip_code = second_form.cleaned_data.get('company_zip_code')
        zip_code_data = parse_zipcode_data(settings.ZIPCODE_DATA_FILE)

        if zip_code in zip_code_data:
            city = zip_code_data[zip_code]['city']
            state = zip_code_data[zip_code]['state']
            company.company_city = city
            company.company_state = state
        else:
            second_form.add_error('company_zip_code', "Invalid Zip Code")
            return self.form_invalid(form, second_form)
            

        company.save()  # Save Company form data

        user = form.save(commit=False)
        user.is_owner = True
        user.is_employee = False
        user.company = company

        user.save()  # Save User form data

        Owner.objects.create(
            user=user,
            company=company
        )
        return super().form_valid(form)
    
    def form_invalid(self, form, second_form):
        context = self.get_context_data(form=form, second_form=second_form)
        context['form_errors'] = form.errors
        context['second_form_errors'] = second_form.errors
        return self.render_to_response(context)
        

    


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plan_list"] = Plan.objects.all()
        return context



class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "customers/client_update.html"
    form_class = ClientCreateForm
    context_object_name = "client-update"

    def get_success_url(self):
        return reverse("customers:client-list")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_owner or user.is_employee:
            queryset = Client.objects.filter(company=user.company)
            queryset = queryset.filter(company=self.request.user.company)
        else:
            return KeyError("User does not have permission to edit clients")
        return queryset
    
    def form_valid(self, form):
        client_first_name = form.cleaned_data.get('client_first_name')
        client_last_name = form.cleaned_data.get('client_last_name')
        client_phone = form.cleaned_data.get('client_phone')

        if client_first_name == '' or client_last_name == '' or client_phone == '':
            form.add_error('client_first_name', "This field is required.")
            form.add_error('client_last_name', "This field is required.")
            form.add_error('client_phone', "This field is required.")
            return self.form_invalid(form)
        
        
        return super().form_valid(form)
    



class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "customers/client_delete.html"
    context_object_name = "client-delete"

    def get_success_url(self):
        return reverse("customers:client-list")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_owner:
            queryset = Client.objects.filter(company=user.company)
            queryset = queryset.filter(company=self.request.user.company)
        else:
            return KeyError("User does not have permission to delete clients")
        return queryset

    def delete(self, request, *args, **kwargs):
        client = self.get_object()
        client.delete()
        return HttpResponseRedirect(self.get_success_url())




# class ClientCreateView(LoginRequiredMixin, generic.CreateView):
#     template_name = "customers/client_create.html"
#     form_class = ClientCreateForm

#     def get_success_url(self):
#         return reverse("customers:client-list")

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_owner or user.is_employee:
#             queryset = Client.objects.filter(company=user.company)
#             queryset = queryset.filter(company=self.request.user.company)
#         else:
#             return KeyError("User does not have permission to create clients")
#         return queryset


#     def form_valid(self, form):
#         client = form.save(commit=False)
#         client.company = self.request.user.company
#         client.user = self.request.user
#         client.save()
#         # TODO send email
#         send_mail(
#             subject="New Client has been created", 
#             message="Go to the site to see the new client",
#             from_email="test@test.com",
#             recipient_list=["test2@test.com"]
#         )
#         return super(ClientCreateView, self).form_valid(form)
