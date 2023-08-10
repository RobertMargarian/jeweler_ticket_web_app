from django.urls import path
from .views import (
    OrderListView, OrderUpdateView, OrderCreateView, OrderDeleteView, ClientListView, ClientUpdateView, ClientCreateView, ClientDeleteView
)
app_name = "customers"

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/order_update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/order_delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('order_create/', OrderCreateView.as_view(), name='order-create'),
    path('client_create/', ClientCreateView.as_view(), name='client-create'),
    path('client_list/', ClientListView.as_view(), name='client-list'),
    path('<int:pk>/client_update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/client_delete/', ClientDeleteView.as_view(), name='client-delete'),
]


""" order_list, order_create, order_update, order_delete, client_list, client_create, client_update, client_delete,
"""