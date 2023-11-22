from typing import Any, Dict
import json, uuid
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import reverse, render, redirect
from django.views import generic, View
from django.views.generic.edit import FormView
from customers.models import Order, Company, Client, User, Note
from django.forms import modelformset_factory, formset_factory
from .forms import OrderCreateForm, PaginationForm
from customers.forms import ClientCreateForm
from customers.mixins import  CompanyOwnerRequiredMixin, EmployeeRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Q
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class Client_AutoComplete(LoginRequiredMixin, generic.View):
    def get(self, request):
        client_search_query = request.GET.get('term', '')
        clients = Client.objects.filter(deleted_flag=False)
        for term in client_search_query.split():
            clients = clients.filter(Q(client_first_name__icontains=term) |
                                    Q(client_last_name__icontains=term) |
                                    Q(client_email__icontains=term) |
                                    Q(client_phone__icontains=term))

        # Creating a list of dictionaries where each dictionary contains id and text keys.
        results = [
            {
                'id': client.id,  # Assuming each client has a unique id
                'text': f"{client.client_first_name} {client.client_last_name} | {client.client_email} | {client.client_phone}"
            }
            for client in clients
        ]
        return JsonResponse(results, safe=False)



class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order_list.html"
    context_object_name = "order_list"

    def get_paginate_by(self, queryset):
        return self.request.user.pref_orders_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # page size setup
        page_size = self.request.GET.get('page_size', self.request.user.pref_orders_per_page)
        context['orders_per_page'] = page_size
        context['pagination_form_orders'] = \
            PaginationForm(initial={'page_size': page_size})
        
        # Order status setup
        context['all_possible_statuses'] = ['Completed', 'Cancelled', 'In Progress']
        context['selected_statuses'] = self.request.GET.getlist('order_status')

        ordert_statuses_query_dict = QueryDict(mutable=True)
        ordert_statuses_query_dict.setlist('order_status', self.request.GET.getlist('order_status'))
        context['order_status_query_string'] = ordert_statuses_query_dict.urlencode()

        # Client search setup
        context['selected_clients'] = self.request.GET.getlist('client_id')
        context['selected_clients_info'] = Client.objects.filter(
            id__in=context['selected_clients'],
            company=self.request.user.company,
            deleted_flag=False
            ).values_list(
                'id',
                'client_first_name',
                'client_last_name',
                'client_email',
                'client_phone'
            )
        
        client_ids_query_dict = QueryDict(mutable=True)
        client_ids_query_dict.setlist('client_id', self.request.GET.getlist('client_id'))
        context['client_ids_query_string'] = client_ids_query_dict.urlencode()

        # Sort by setup
        context['sort_by'] = self.request.GET.get('sort_by', 'work_order_date')

        return context
    
    def get_queryset(self):
        user = self.request.user
        statuses = self.request.GET.getlist('order_status', None)
        client_ids = self.request.GET.getlist('client_id', None)
        sort_by = self.request.GET.get('sort_by', '-created_at')

        if sort_by.replace('-', '') not in ['work_order_date', 'work_order_due_date']:
            sort_by = '-created_at'

        if user.is_owner or user.is_employee:
            queryset = Order.objects \
                .filter(company=user.company) \
                .filter(deleted_flag=False) \
                .filter(client__company=user.company)
            
            if statuses:
                queryset = queryset.filter(work_order_status__in = statuses)

            if client_ids:
                queryset = queryset.filter(client__id__in = client_ids)
                                            
            queryset = queryset.order_by(sort_by)
        else:
            return KeyError("User does not have permission to view orders")
        return queryset

    def get(self, request, *args, **kwargs):
        # Check if page_size is being updated
        if 'page_size' in request.GET:
            try:
                page_size = request.GET.get('page_size')
                # Update the user's preference in the model
                request.user.pref_orders_per_page = page_size
                request.user.save()
            except ValueError:
                pass
        return super().get(request, *args, **kwargs)




class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "orders/order_create.html"
    form_class = OrderCreateForm
    context_object_name = "order-create"

    def get_success_url(self):
        return reverse("orders:order-list")

    def form_valid(self, form):   
        client_already_exists = self.request.POST.get('client_already_exists')
        client_form = ClientCreateForm(self.request.POST)
        
        if form.is_valid() and client_form.is_valid():
            user = self.request.user
            order = form.save(commit=False)
            order.company = user.company
            order.user = user
            order_photo = self.request.FILES.get('order_photo')
            if order_photo and order_photo.size > (6 * 1024 * 1024):  # 6 MB
                form.add_error('order_photo', "File size should not exceed 6 MB.")
                return self.form_invalid(form)
            
            if client_already_exists == 'True':
                if 'client' in form.cleaned_data and form.cleaned_data['client']:
                    order.client = form.cleaned_data['client']
                    order.work_order_currency = "USD"
                    order.quoted_currency = "USD"
                    order.save() 
                else:
                    form.add_error('client', "Client must be selected when Client Already Exists is checked.")

            elif client_already_exists == 'False':
                if (client_form.cleaned_data.get('client_first_name') != ''
                    and client_form.cleaned_data.get('client_last_name') != ''
                    and client_form.cleaned_data.get('client_phone') != ''
                    ):
                    client = Client.objects.create(
                        company=user.company,
                        user = user,
                        client_first_name=client_form.cleaned_data['client_first_name'],
                        client_last_name=client_form.cleaned_data['client_last_name'],
                        client_email=client_form.cleaned_data['client_email'],
                        client_phone=client_form.cleaned_data['client_phone'],
                        client_check_mobile_phone=client_form.cleaned_data['client_check_mobile_phone'],
                    )
                    order.client = client
                    client.save()
                    # order.work_order_status = "In Progress"
                    order.work_order_currency = "USD"
                    order.quoted_currency = "USD"
                    order.save()

                else:
                    form.add_error('client', "Create a new client or check the box.")

            note_content = self.request.POST.get('note_content')

            if note_content:
                # Create a new note and associate it with the current order
                note = Note.objects.create(order=order, content=note_content)
                note.user = user
                note.company = user.company
                note.save()           

            if not form.is_valid() or not client_form.is_valid():
                return self.form_invalid(form)
        
            return redirect(self.get_success_url())
        
        return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = kwargs.get('client_form', ClientCreateForm())
        return context



class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    template_name = "orders/order_update.html"
    form_class = OrderCreateForm
    context_object_name = "order-update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter notes associated with the order, excluding deleted notes
        context['notes'] = Note.objects.filter(order=self.object, deleted_flag=False)
        return context

    def get_success_url(self):
        return reverse("orders:order-list")
    
    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(company=user.company)

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        order_photo = self.request.FILES.get('order_photo')

        if order_photo and order_photo.size > (6 * 1024 * 1024):  # 6 MB
            form.add_error('order_photo', "File size should not exceed 6 MB.")
            return self.form_invalid(form)
        
        order.save()
        
        # Check for a new note in the request POST data
        note_content = self.request.POST.get('note_content')
        note_action = self.request.META.get('HTTP_X_NOTE_ACTION')

        if note_content and note_action == 'create':
            # Create a new note and associate it with the current order
            note = Note.objects.create(order=order, content=note_content)
            note.user = user
            note.company = user.company
            note.save()
        
        return super().form_valid(form)
    
    

class AddNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note_content = request.POST.get('note_content')
        if note_content:
            # Create a new note and associate it with the order (pk)
            note = Note.objects.create(order_id=pk, content=note_content, user=request.user, company=request.user.company)
            return JsonResponse({'success': True, 'note_id': note.id, 'timestamp': note.timestamp})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid note content.'})
        

# class NoteDeleteView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         try:
#             note_id = request.POST.get('note_id') 
#             print("Received note ID:", note_id)
#             note = Note.objects.get(pk=note_id)
#             if note_id is not None:
#                 note_id = int(note_id)
                

#                 # Soft delete the note by setting the `deleted_flag` to True
#                 note.deleted_flag = True
#                 note.save()

#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'success': False, 'error': 'Note ID is missing or not valid'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
        
class NoteDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # Use self.kwargs to access URL parameters
            note_id = self.kwargs.get('pk')

            # Check if note_id is a valid UUID
            try:
                uuid_obj = uuid.UUID(note_id)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid note ID'})
            
            # Use get_object_or_404 to get the Note object or return a 404 response if not found
            note = get_object_or_404(Note, pk=note_id)

            # Soft delete the note by setting the `deleted_flag` to True
            note.deleted_flag = True
            note.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "orders/order_delete.html"
    context_object_name = "order-delete"

    def get_success_url(self):
        return reverse("orders:order-list")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_owner:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to delete orders")
        return queryset