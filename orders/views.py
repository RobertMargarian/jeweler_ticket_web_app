from typing import Any, Dict
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import reverse, render, redirect
from django.views import generic
from customers.models import Order, Company, Client, User
from .forms import OrderCreateForm, PaginationForm
from customers.mixins import  CompanyOwnerRequiredMixin, CompanyAdminRequiredMixin
from django.contrib.auth.decorators import login_required


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
        return context

    
    def get_queryset(self):
        user = self.request.user
        if user.user_role in [1, 2, 3]:
            queryset = Order.objects \
                .filter(company=user.company) \
                .filter(client__company=user.company) \
                .order_by('-created_at')
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

    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "orders/order_create.html"
    redirect_template_name = "orders/order_list.html"
    form_class = OrderCreateForm
    context_object_name = "order-create"
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = self.form_class(user=user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        form = self.form_class(user=user, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.company = self.request.user.company
            order.work_order_status = "In Progress"
            order.save()
            # TODO send email
            send_mail(
                subject="New Order has been created", 
                message="Go to the site to see the new order",
                from_email="test@test.com",
                recipient_list=["test2@test.com"]
            )
            return redirect(self.get_success_url())
        context = {'form': form}
        return render(request, self.redirect_template_name, context)
    
    def get_success_url(self):
        return reverse("orders:order-list")


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
        if user.user_role in [1, 2, 3]:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to delete orders")
        return queryset