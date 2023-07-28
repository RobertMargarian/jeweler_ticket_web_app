from django.urls import path
from .views import orders, order_detail, customers, customer_detail, order_create


urlpatterns = [
    path('', orders),
    path('order_create/', order_create),
    path('<int:pk>/', order_detail),
    path('customers/', customers),
    path('customers/<int:pk>/', customer_detail)
]
