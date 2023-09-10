from typing import Any
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import reverse, render, redirect
from django.db.models import Sum
from django.views import generic
from .models import Order, Client, Company, User, Plan, Owner
from django.views.generic.edit import FormView
from .forms import ClientCreateForm, CustomUserCreationForm, CompanyCreateForm, PaginationForm
from .mixins import  CompanyOwnerRequiredMixin, EmployeeRequiredMixin 
# should use this mixin for all views that require login and role

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    second_form_class = CompanyCreateForm
    success_url = '/login/'  # Redirect URL after successful form submission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['second_form'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        second_form = self.second_form_class(request.POST)

        if form.is_valid() and second_form.is_valid():
            return self.form_valid(form, second_form)
        else:
            return self.form_invalid(form, second_form)

    def form_valid(self, form, second_form):
        company = second_form.save(commit=False)
        company.company_current_plan = Plan.objects.get(id=3)
        company.company_subscription_status = "Active"
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
    

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plan_list"] = Plan.objects.all()
        return context


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = "customers/client_list.html"
    context_object_name = "client_list"

    def get_paginate_by(self, queryset):
        return self.request.user.pref_clients_per_page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form with the user's preference
        context['pagination_form_clients'] = \
            PaginationForm(initial={'page_size': self.request.user.pref_clients_per_page})
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_owner or user.is_employee: 
            queryset = Client.objects \
                .filter(company=user.company) \
                .filter(company=self.request.user.company) \
                .filter(deleted_flag=False) \
                .order_by('-created_at') \
                .filter(company=self.request.user.company).annotate(
                    total_spent_column=Sum('order__quoted_price')
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








# def order_create(request):
#     form_order_create = OrderCreateForm()
#     if request.method == "POST":
#         form_order_create = OrderCreateForm(request.POST)
#         if form_order_create.is_valid():
#             form_order_create.save()
#             return redirect('/')
#     context = {
#         "form_order": form_order_create
#     }
#     return render(request, "customers/order_create.html", context)


# def order_list(request):
#     order_list = Order.objects.all()
#     client_list = Client.objects.all()
#     context = {
#         "order_list": order_list,
#         "client_list": client_list
#     }
#     return render(request, "customers/order_list.html", context)




# def client_delete(request, pk):
#     client = Client.objects.get(id=pk)
#     client.delete()
#     return redirect("/client_list/")



# def order_update(request, pk):
#     order = Order.objects.get(id=pk)
#     client = Client.objects.get(id=order.client_id)
#     form_order = OrderCreateForm(instance=order)
#     form_client = ClientCreateForm(instance=client)
#     if request.method == "POST":
#         form_order = OrderCreateForm(request.POST, instance=order)
#         form_client = ClientCreateForm(request.POST, instance=client)
#         if form_order.is_valid() and form_client.is_valid():
#             form_order.save()
#             form_client.save()
#             return redirect('/')
#     context = {
#         "order": order,
#         "client": client,
#         "form_order": form_order,
#         "form_client": form_client
#     }
#     return render(request, "customers/order_update.html", context)


# def client_create(request):
#     form = ClientCreateForm()
#     if request.method == "POST":
#         form = ClientCreateForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             Client.objects.create(
#             client_first_name = form.cleaned_data['client_first_name'],
#             client_last_name = form.cleaned_data['client_last_name'],
#             client_email = form.cleaned_data['client_email'],
#             client_phone = form.cleaned_data['client_phone'],
#             client_check_mobile_phone = form.cleaned_data['client_check_mobile_phone']
#             )
#             form.save()
#             return redirect('/order_create/')
#     context = {
#         "form": form
#     }
#     return render(request, "customers/client_create.html", context)



# def order_delete(request, pk):
#     order = Order.objects.get(id=pk)
#     order.delete()
#     return redirect("/")

# def client_list(request):
#     client_list = Client.objects.all()
#     context = {
#         "client_list": client_list
#     }
#     return render(request, "customers/client_list.html", context)

# def order_create(request):
#     form_client_check = ClientCheckForm()
#     form_client = ClientCreateForm()
#     form_order = OrderCreateForm()
#     if request.method == "POST":
#         form_client_check = ClientCheckForm()
#         form_client = ClientCreateForm()
#         form_order = OrderCreateForm()
#         if form_client_check.is_valid() and form_client.is_valid() and form_order.is_valid():
#             print(form_client_check.cleaned_data)
#             if form_client_check.cleaned_data['client_already_exists'] == True:
#                 print(form_order.cleaned_data)
#                 Order.objects.create(
#                     client = form_client.cleaned_data['client'],
#                     estimated_cost = form_order.cleaned_data['estimated_cost'],
#                     quoted_price = form_order.cleaned_data['quoted_price'],
#                     security_deposit = form_order.cleaned_data['security_deposit'],
#                     work_order_type = form_order.cleaned_data['work_order_type'],
#                     work_order_status = form_order.cleaned_data['work_order_status']
#                 )
#                 form_client_check.save()
#                 form_client.save()
#                 form_order.save()
#             else:
#                 Client.objects.create(
#                     client_first_name = form_client.cleaned_data['client_first_name'],
#                     client_last_name = form_client.cleaned_data['client_last_name'],
#                     client_email = form_client.cleaned_data['client_email'],
#                     client_phone = form_client.cleaned_data['client_phone'],
#                     client_check_mobile_phone = form_client.cleaned_data['client_check_mobile_phone']
#                 )
#                 Order.objects.create(
#                     client = form_client.cleaned_data['client'],
#                     estimated_cost = form_order.cleaned_data['estimated_cost'],
#                     quoted_price = form_order.cleaned_data['quoted_price'],
#                     security_deposit = form_order.cleaned_data['security_deposit'],
#                     work_order_type = form_order.cleaned_data['work_order_type'],
#                     work_order_status = form_order.cleaned_data['work_order_status']
#                 )
#                 form_client_check.save()
#                 form_client.save()
#                 form_order.save()
#             return redirect('/')
#     context = {
#         "form_client_check": form_client_check,
#         "form_client": form_client,
#         "form_order": form_order
#     }
#     return render(request, "customers/order_create.html", context)



            # Order.objects.create(
            #     client = form_order.cleaned_data['client'],
            #     work_order_type = form_order.cleaned_data['work_order_type'],
            #     estimated_cost = form_order.cleaned_data['estimated_cost'],
            #     quoted_price = form_order.cleaned_data['quoted_price'],
            #     security_deposit = form_order.cleaned_data['security_deposit'],
            #     work_order_date = form_order.cleaned_data['work_order_date'],
            #     work_order_due_date = form_order.cleaned_data['work_order_due_date'],
            #     work_order_status = form_order.cleaned_data['work_order_status']
            # )


# def client_create(request):
#     form_client_create = ClientCreateForm()
#     if request.method == "POST":
#         form_client_create = ClientCreateForm(request.POST)
#         if form_client_create.is_valid():
#             print(form_client_create.cleaned_data)
#             form_client_create.save()
#             return redirect('/')
#     context = {
#         "form_client_create": form_client_create
#     }
#     return render(request, "customers/client_create.html", context)

# def client_update(request, pk):
#     client = Client.objects.get(id=pk)
#     form_client_update = ClientCreateForm(instance=client)
#     if request.method == "POST":
#         form_client_update = ClientCreateForm(request.POST, instance=client)
#         if form_client_update.is_valid():
#             form_client_update.save()
#             return redirect('/client_list/')
#     context = {
#         "client": client,
#         "form_client_update": form_client_update
#     }
#     return render(request, "customers/client_update.html", context)

# if form_client.cleaned_data['client_already_exists'] == True:
#                 Order.objects.create(
#                     client = form_client.cleaned_data['client'],
#                     estimated_cost = form_order.cleaned_data['estimated_cost'],
#                     quoted_price = form_order.cleaned_data['quoted_price'],
#                     security_deposit = form_order.cleaned_data['security_deposit'],
#                     work_order_type = form_order.cleaned_data['work_order_type'],
#                     work_order_status = form_order.cleaned_data['work_order_status']
#                 )
#                 form_client.save()
#                 form_order.save()
#             else:
#                 Client.objects.create(
#                     client_first_name = form_client.cleaned_data['client_first_name'],
#                     client_last_name = form_client.cleaned_data['client_last_name'],
#                     client_email = form_client.cleaned_data['client_email'],
#                     client_phone = form_client.cleaned_data['client_phone'],
#                     client_check_mobile_phone = form_client.cleaned_data['client_check_mobile_phone']
#                 )
#                 Order.objects.create(
#                     client = form_client.cleaned_data['client'],
#                     estimated_cost = form_order.cleaned_data['estimated_cost'],
#                     quoted_price = form_order.cleaned_data['quoted_price'],
#                     security_deposit = form_order.cleaned_data['security_deposit'],
#                     work_order_type = form_order.cleaned_data['work_order_type'],
#                     work_order_status = form_order.cleaned_data['work_order_status']
#                 )
#                 form_client.save()
#                 form_order.save()