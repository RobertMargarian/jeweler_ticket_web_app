from django.urls import path
from .views import (
    OrderListView, OrderUpdateView, OrderCreateView, OrderDeleteView, Client_AutoComplete, AddNoteView ,NoteDeleteView
)

app_name = "orders"

urlpatterns = [
    path('order_list/', OrderListView.as_view(), name='order-list'),
    path('client-autocomplete/', Client_AutoComplete.as_view(), name='client-autocomplete'),
    path('order_create/', OrderCreateView.as_view(), name='order-create'),  
    path('<uuid:pk>/order_update/', OrderUpdateView.as_view(), name='order-update'),
    path('<uuid:pk>/order_delete/', OrderDeleteView.as_view(), name='order-delete'),  
    path('<uuid:pk>/add-note/', AddNoteView.as_view(), name='add-note'),
    path('<pk>/note_delete/', NoteDeleteView.as_view(), name='note-delete'),
]
