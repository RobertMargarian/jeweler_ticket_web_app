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

class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order_list.html"
    queryset = Order.objects.all()
    context_object_name = "order_list"

"""     def get_queryset(self):
        company = self.request.user.company
        return Order.objects.filter(company=company) """

    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "orders/order_create.html"
    form_class = OrderCreateForm

    def get_success_url(self):
        return reverse("orders:order-list")

    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="New Order has been created", 
            message="Go to the site to see the new order",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(OrderCreateView, self).form_vordersalid(form)


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "orders/order_update.html"
    queryset = Order.objects.all()
    form_class = OrderCreateForm
    context_object_name = "order-update"

    def get_success_url(self):
        return reverse("orders:order-list")

"""     def get_queryset(self):
        company = self.request.user.company
        return Order.objects.filter(company=company) """


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "orders/order_delete.html"
    queryset = Order.objects.all()
    context_object_name = "order-delete"

    def get_success_url(self):
        return reverse("orders:order-list")
    
"""     def get_queryset(self):
        company = self.request.user.company
        return Order.objects.filter(company=company) """