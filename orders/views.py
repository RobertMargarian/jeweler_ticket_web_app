from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic
from customers.models import Order
from .forms import OrderCreateForm
from customers.mixins import  CompanyOwnerRequiredMixin, CompanyAdminRequiredMixin


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "orders/order_list.html"
    context_object_name = "order_list"

    def get_paginate_by(self, queryset):
        # Get the page_size from the query parameters, default to 10 if not provided
        return self.request.GET.get('page_size', 10)
    
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

    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "orders/order_create.html"
    form = OrderCreateForm() 
    form_class = OrderCreateForm

    def get_queryset(self):
        form = OrderCreateForm()
        user = self.request.user
        if user.user_role in [1, 2, 3]:
            form.fields['client'].queryset = form.fields['client'].queryset.filter(company=user.company)
        else:
            return KeyError("User does not have permission to create orders")
        return form

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
        if user.user_role in [1, 2, 3]:
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
        if user.user_role in [1, 2, 3]:
            queryset = Order.objects.filter(company=user.company)
            queryset = queryset.filter(client__company=user.company)
        else:
            return KeyError("User does not have permission to delete orders")
        return queryset