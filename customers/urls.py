from django.urls import path
from .views import orders, order_detail, customers, customer_detail


urlpatterns = [
    path('', orders),
    path('<int:pk>/', order_detail),
    path('customers/', customers),
    path('customers/<int:pk>/', customer_detail)
]
