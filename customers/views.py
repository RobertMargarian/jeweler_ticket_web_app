from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Company, User, Order, Client, Plan
from .forms import OrderCreateForm, ClientCreateForm


def orders(request):
    orders = Order.objects.all()
    context = {
        "orders": orders
    }
    return render(request, "customers/orders.html", context)


def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return render(request, "customers/orders.html")


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    client = Client.objects.get(id=order.client_id)
    context = {
        "order": order,
        "client": client
    }
    return render(request, "customers/order_detail.html", context)


def order_create(request):
    form = OrderCreateForm()
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Order.objects.create(
                estimated_cost = form.cleaned_data['estimated_cost'],
                quoted_price = form.cleaned_data['quoted_price'],
                security_deposit = form.cleaned_data['security_deposit'],
                work_order_type = form.cleaned_data['work_order_type'],
                work_order_status = form.cleaned_data['work_order_status']
            )
            return redirect('/')
    context = {
        "form": form
    }
    return render(request, "customers/order_create.html", context)


def customer_create(request):
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
            return redirect('/')
    context = {
        "form": form
    }
    return render(request, "customers/order_create.html", context)



def customers(request):
    customers = Client.objects.all()
    context = {
        "customers": customers
    }
    return render(request, "customers/customers.html", context)


def customer_delete(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    return render(request, "customers/customers.html")


def customer_detail(request, pk):
    client = Client.objects.get(id=pk)
    context = {
        "client": client
    }
    return render(request, "customers/customer_detail.html", context)
