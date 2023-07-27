from django.shortcuts import render
from django.http import HttpResponse
from .models import Company, User, Order, Client, User_Role, Plan


def orders(request):
    orders = Order.objects.all()
    context = {
        "orders": orders
    }
    return render(request, "customers/orders.html", context)


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    context = {
        "order": order
    }
    return render(request, "customers/order_detail.html", context)

