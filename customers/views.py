from django.shortcuts import render
from django.http import HttpResponse
from .models import Company, User, Order, Client, Plan
from .forms import OrderForm


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
    form = OrderForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = OrderForm(request.POST)
        if form.is_valid():
            print('Form is valid')
            print(form.cleaned_data)
            Client.objects.create(
                client_first_name = form.cleaned_data['client_first_name'],
                client_last_name = form.cleaned_data['client_last_name'],
                client_email = form.cleaned_data['client_email'],
                client_phone = form.cleaned_data['client_phone'],
                client_check_mobile_phone = form.cleaned_data['client_check_mobile_phone']
            )
            Order.objects.create(
                work_order_date = form.cleaned_data['work_order_date'],
                work_order_due_date = form.cleaned_data['work_order_due_date'],
                estimated_cost = form.cleaned_data['estimated_cost'],
                quoted_price = form.cleaned_data['quoted_price'],
                security_deposit = form.cleaned_data['security_deposit'],
                work_order_type = form.cleaned_data['work_order_type'],
                work_order_status = form.cleaned_data['work_order_status']
            )
            print('Order has been created')
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
