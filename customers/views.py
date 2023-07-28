from django.shortcuts import render
from django.http import HttpResponse
from .models import Company, User, Order, Client, Plan


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
