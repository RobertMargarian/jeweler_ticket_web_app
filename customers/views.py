from django.shortcuts import render
from django.http import HttpResponse
from .models import Company, User, Order, Client, User_Role, Plan


def orders(request):
    orders = Order.objects.all()
    context = {
        "orders": orders
    }
    return render(request, "orders.html", context)

