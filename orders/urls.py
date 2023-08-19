from django.urls import path
from .views import (
    OrderListView, OrderUpdateView, OrderCreateView, OrderDeleteView
)

app_name = "orders"

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/order_update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/order_delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('order_create/', OrderCreateView.as_view(), name='order-create'),    
]
