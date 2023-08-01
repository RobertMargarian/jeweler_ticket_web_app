from django.urls import path
from .views import orders, order_detail, customers, customer_detail, order_create, customer_create


urlpatterns = [
    path('', orders),
    path('<int:pk>/', order_detail),
    path('order_create/', order_create),
    path('customer_create/', customer_create),
    path('customers/', customers),
    path('customers/<int:pk>/', customer_detail)
]
