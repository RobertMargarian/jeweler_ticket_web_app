from typing import Any, Dict
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import reverse, render, redirect
from django.views import generic
from django.views.generic.edit import FormView
from customers.models import Order, Company, Client, User
from django.forms import modelformset_factory, formset_factory
from .forms import OrderCreateForm, PaginationForm, OrderStatusFilterForm
from customers.forms import ClientCreateForm
from customers.mixins import  CompanyOwnerRequiredMixin, EmployeeRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.db.transaction import atomic


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order_list.html"
    context_object_name = "order_list"

    def get_paginate_by(self, queryset):
        return self.request.user.pref_orders_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form with the user's preference
        context['pagination_form_orders'] = \
            PaginationForm(initial={'page_size': self.request.user.pref_orders_per_page})
        
        context['filter_form'] = OrderStatusFilterForm(self.request.GET)
        context['selected_statuses'] = self.request.GET.getlist('order_status')
        context['orders_per_page'] = self.request.user.pref_orders_per_page
        context['all_possible_statuses'] = ['Completed', 'Cancelled', 'In Progress']
        return context

    
    def get_queryset(self):
        user = self.request.user
        statuses = self.request.GET.getlist('order_status')

        if user.is_owner or user.is_employee:
            queryset = Order.objects \
                .filter(company=user.company) \
                .filter(deleted_flag=False) \
                .filter(client__company=user.company)
            
            if statuses:
                queryset = queryset.filter(work_order_status__in = statuses)

            queryset = queryset.order_by('-created_at')
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

            if client_already_exists == 'True':
                if 'client' in form.cleaned_data and form.cleaned_data['client']:
                    order.client = form.cleaned_data['client']
                    order.work_order_status = "In Progress"
                    order.work_order_currency = "USD"
                    order.quoted_currency = "USD"
                    order.order_photo = self.request.FILES.get('order_photo')
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
                    order.work_order_status = "In Progress"
                    order.work_order_currency = "USD"
                    order.quoted_currency = "USD"
                    order.order_photo = self.request.FILES.get('order_photo')
                    order.save()

                else:
                    form.add_error('client', "Create a new client or check the box.")


            if not form.is_valid() or not client_form.is_valid() or (not form.is_valid() and not client_form.is_valid()):
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
        return super().form_valid(form)

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