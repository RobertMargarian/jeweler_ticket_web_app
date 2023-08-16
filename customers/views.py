from django.core.mail import send_mail
from typing import Any
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from .models import Order, Client, Company, User, Plan
from .forms import OrderCreateForm, ClientCreateForm, CustomUserCreationForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = "customers/order_list.html"
    queryset = Order.objects.all()
    context_object_name = "order_list"

    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "customers/order_create.html"
    form_class = OrderCreateForm

    def get_success_url(self):
        return reverse("customers:order-list")

    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="New Order has been created", 
            message="Go to the site to see the new order",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "customers/order_update.html"
    form_class = OrderCreateForm
    queryset = Order.objects.all()
    context_object_name = "order-update"

    def get_success_url(self):
        return reverse("customers:order-list")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "customers/order_delete.html"
    queryset = Order.objects.all()
    context_object_name = "order-delete"

    def get_success_url(self):
        return reverse("customers:order-list")


class ClientListView(LoginRequiredMixin, generic.ListView):
    template_name = "customers/client_list.html"
    queryset = Client.objects.all()
    context_object_name = "client_list"


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "customers/client_create.html"
    form_class = ClientCreateForm

    def get_success_url(self):
        return reverse("customers:client-list")

    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="New Client has been created", 
            message="Go to the site to see the new client",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "customers/client_update.html"
    form_class = ClientCreateForm
    queryset = Client.objects.all()
    context_object_name = "client-update"

    def get_success_url(self):
        return reverse("customers:client-list")


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "customers/client_delete.html"
    queryset = Client.objects.all()
    context_object_name = "client-delete"

    def get_success_url(self):
        return reverse("customers:client-list")







""" def order_create(request):
    form_order_create = OrderCreateForm()
    if request.method == "POST":
        form_order_create = OrderCreateForm(request.POST)
        if form_order_create.is_valid():
            form_order_create.save()
            return redirect('/')
    context = {
        "form_order": form_order_create
    }
    return render(request, "customers/order_create.html", context) """


""" def order_list(request):
    order_list = Order.objects.all()
    client_list = Client.objects.all()
    context = {
        "order_list": order_list,
        "client_list": client_list
    }
    return render(request, "customers/order_list.html", context) """




""" def client_delete(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    return redirect("/client_list/") """



""" def order_update(request, pk):
    order = Order.objects.get(id=pk)
    client = Client.objects.get(id=order.client_id)
    form_order = OrderCreateForm(instance=order)
    form_client = ClientCreateForm(instance=client)
    if request.method == "POST":
        form_order = OrderCreateForm(request.POST, instance=order)
        form_client = ClientCreateForm(request.POST, instance=client)
        if form_order.is_valid() and form_client.is_valid():
            form_order.save()
            form_client.save()
            return redirect('/')
    context = {
        "order": order,
        "client": client,
        "form_order": form_order,
        "form_client": form_client
    }
    return render(request, "customers/order_update.html", context) """

""" 
def client_create(request):
    form = ClientCreateForm()
    if request.method == "POST":
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Client.objects.create(
            client_first_name = form.cleaned_data['client_first_name'],
            client_last_name = form.cleaned_data['client_last_name'],
            client_email = form.cleaned_data['client_email'],
            client_phone = form.cleaned_data['client_phone'],
            client_check_mobile_phone = form.cleaned_data['client_check_mobile_phone']
            )
            form.save()
            return redirect('/order_create/')
    context = {
        "form": form
    }
    return render(request, "customers/client_create.html", context)

"""

""" def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect("/") """

""" def client_list(request):
    client_list = Client.objects.all()
    context = {
        "client_list": client_list
    }
    return render(request, "customers/client_list.html", context) """

""" def order_create(request):
    form_client_check = ClientCheckForm()
    form_client = ClientCreateForm()
    form_order = OrderCreateForm()
    if request.method == "POST":
        form_client_check = ClientCheckForm()
        form_client = ClientCreateForm()
        form_order = OrderCreateForm()
        if form_client_check.is_valid() and form_client.is_valid() and form_order.is_valid():
            print(form_client_check.cleaned_data)
            if form_client_check.cleaned_data['client_already_exists'] == True:
                print(form_order.cleaned_data)
                Order.objects.create(
                    client = form_client.cleaned_data['client'],
                    estimated_cost = form_order.cleaned_data['estimated_cost'],
                    quoted_price = form_order.cleaned_data['quoted_price'],
                    security_deposit = form_order.cleaned_data['security_deposit'],
                    work_order_type = form_order.cleaned_data['work_order_type'],
                    work_order_status = form_order.cleaned_data['work_order_status']
                )
                form_client_check.save()
                form_client.save()
                form_order.save()
            else:
                Client.objects.create(
                    client_first_name = form_client.cleaned_data['client_first_name'],
                    client_last_name = form_client.cleaned_data['client_last_name'],
                    client_email = form_client.cleaned_data['client_email'],
                    client_phone = form_client.cleaned_data['client_phone'],
                    client_check_mobile_phone = form_client.cleaned_data['client_check_mobile_phone']
                )
                Order.objects.create(
                    client = form_client.cleaned_data['client'],
                    estimated_cost = form_order.cleaned_data['estimated_cost'],
                    quoted_price = form_order.cleaned_data['quoted_price'],
                    security_deposit = form_order.cleaned_data['security_deposit'],
                    work_order_type = form_order.cleaned_data['work_order_type'],
                    work_order_status = form_order.cleaned_data['work_order_status']
                )
                form_client_check.save()
                form_client.save()
                form_order.save()
            return redirect('/')
    context = {
        "form_client_check": form_client_check,
        "form_client": form_client,
        "form_order": form_order
    }
    return render(request, "customers/order_create.html", context)
"""


"""             Order.objects.create(
                client = form_order.cleaned_data['client'],
                work_order_type = form_order.cleaned_data['work_order_type'],
                estimated_cost = form_order.cleaned_data['estimated_cost'],
                quoted_price = form_order.cleaned_data['quoted_price'],
                security_deposit = form_order.cleaned_data['security_deposit'],
                work_order_date = form_order.cleaned_data['work_order_date'],
                work_order_due_date = form_order.cleaned_data['work_order_due_date'],
                work_order_status = form_order.cleaned_data['work_order_status']
            ) """


""" def client_create(request):
    form_client_create = ClientCreateForm()
    if request.method == "POST":
        form_client_create = ClientCreateForm(request.POST)
        if form_client_create.is_valid():
            print(form_client_create.cleaned_data)
            form_client_create.save()
            return redirect('/')
    context = {
        "form_client_create": form_client_create
    }
    return render(request, "customers/client_create.html", context) """

""" def client_update(request, pk):
    client = Client.objects.get(id=pk)
    form_client_update = ClientCreateForm(instance=client)
    if request.method == "POST":
        form_client_update = ClientCreateForm(request.POST, instance=client)
        if form_client_update.is_valid():
            form_client_update.save()
            return redirect('/client_list/')
    context = {
        "client": client,
        "form_client_update": form_client_update
    }
    return render(request, "customers/client_update.html", context) """

""" if form_client.cleaned_data['client_already_exists'] == True:
                Order.objects.create(
                    client = form_client.cleaned_data['client'],
                    estimated_cost = form_order.cleaned_data['estimated_cost'],
                    quoted_price = form_order.cleaned_data['quoted_price'],
                    security_deposit = form_order.cleaned_data['security_deposit'],
                    work_order_type = form_order.cleaned_data['work_order_type'],
                    work_order_status = form_order.cleaned_data['work_order_status']
                )
                form_client.save()
                form_order.save()
            else:
                Client.objects.create(
                    client_first_name = form_client.cleaned_data['client_first_name'],
                    client_last_name = form_client.cleaned_data['client_last_name'],
                    client_email = form_client.cleaned_data['client_email'],
                    client_phone = form_client.cleaned_data['client_phone'],
                    client_check_mobile_phone = form_client.cleaned_data['client_check_mobile_phone']
                )
                Order.objects.create(
                    client = form_client.cleaned_data['client'],
                    estimated_cost = form_order.cleaned_data['estimated_cost'],
                    quoted_price = form_order.cleaned_data['quoted_price'],
                    security_deposit = form_order.cleaned_data['security_deposit'],
                    work_order_type = form_order.cleaned_data['work_order_type'],
                    work_order_status = form_order.cleaned_data['work_order_status']
                )
                form_client.save()
                form_order.save() """