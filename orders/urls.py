from django.urls import path
from .views import (
    OrderListView, OrderUpdateView, OrderCreateView, OrderDeleteView, NoteDeleteView
)

app_name = "orders"

urlpatterns = [
    path('order_list/', OrderListView.as_view(), name='order-list'),
    path('order_create/', OrderCreateView.as_view(), name='order-create'),  
    path('<int:pk>/order_update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/order_delete/', OrderDeleteView.as_view(), name='order-delete'),  
    path('<int:pk>/note_delete/', NoteDeleteView.as_view(), name='note-delete'),
]
