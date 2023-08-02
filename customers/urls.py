from django.urls import path
from .views import orders, order_update, customers, customer_detail, order_create, customer_create, order_delete


urlpatterns = [
    path('', orders),
    path('<int:pk>/update/', order_update),
    path('<int:pk>/delete/', order_delete),
    path('order_create/', order_create),
    path('customer_create/', customer_create),
    path('customers/', customers),
    path('customers/<int:pk>/', customer_detail)
]
