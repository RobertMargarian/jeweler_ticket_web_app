from django.urls import path
from .views import (
    ClientListView, ClientUpdateView, ClientDeleteView, Client_AutoComplete
)

app_name = "customers"

urlpatterns = [
    path('client_list/', ClientListView.as_view(), name='client-list'),
    path('client-autocomplete/', Client_AutoComplete.as_view(), name='client-autocomplete'),
    path('<uuid:pk>/client_update/', ClientUpdateView.as_view(), name='client-update'),
    path('<uuid:pk>/client_delete/', ClientDeleteView.as_view(), name='client-delete'),
]
