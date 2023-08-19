from django.urls import path
from .views import (
    ClientListView, ClientUpdateView, ClientCreateView, ClientDeleteView
)

app_name = "customers"

urlpatterns = [
    path('', ClientCreateView.as_view(), name='client-create'),
    path('client_list/', ClientListView.as_view(), name='client-list'),
    path('<int:pk>/client_update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/client_delete/', ClientDeleteView.as_view(), name='client-delete'),
]


"""     path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/order_update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/order_delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('order_create/', OrderCreateView.as_view(), name='order-create'), """
