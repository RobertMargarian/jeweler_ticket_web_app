from django.shortcuts import render
from django.core.mail import send_mail
from typing import Any
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from customers.models import Order
from .forms import OrderCreateForm
from customers.mixins import  CompanyOwnerRequiredMixin, CompanyAdminRequiredMixin, EmployeeRequiredMixin


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order_list.html"
    context_object_name = "order_list"

    def get_queryset(self):
        user = self.request.user
        if user.user_role == 1 or user.user_role == 2 or user.user_role == 3:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to view orders")
        return queryset

    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "orders/order_create.html"
    form = OrderCreateForm() 
    form_class = OrderCreateForm

    def get_queryset(self):
        user = self.request.user
        if user.user_role == 1 or user.user_role == 2 or user.user_role == 3:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
            form.fields['client'].queryset = queryset
        else:
            return KeyError("User does not have permission to create orders")
        return queryset

    def get_success_url(self):
        return reverse("orders:order-list")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.company = self.request.user.company
        order.save()
        # TODO send email
        send_mail(
            subject="New Order has been created", 
            message="Go to the site to see the new order",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "orders/order_update.html"
    form_class = OrderCreateForm
    context_object_name = "order-update"

    def get_success_url(self):
        return reverse("orders:order-list")

    def get_queryset(self):
        user = self.request.user
        if user.user_role == 1 or user.user_role == 2 or user.user_role == 3:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to edit orders")
        return queryset


class OrderDeleteView(CompanyAdminRequiredMixin, CompanyOwnerRequiredMixin, generic.DeleteView):
    template_name = "orders/order_delete.html"
    context_object_name = "order-delete"

    def get_success_url(self):
        return reverse("orders:order-list")
    
    def get_queryset(self):
        user = self.request.user
        if user.user_role == 1 or user.user_role == 2 or user.user_role == 3:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to delete orders")
        return queryset