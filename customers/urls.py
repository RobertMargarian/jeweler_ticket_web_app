from django.urls import path
from .views import orders, order_update, order_create, client_create, order_delete, clients, client_update, client_delete


urlpatterns = [
    path('', orders, name='orders'),
    path('<int:pk>/order_update/', order_update, name='order_update'),
    path('<int:pk>/order_delete/', order_delete, name='order_delete'),
    path('order_create/', order_create, name='order_create'),
    path('client_create/', client_create, name='client_create'),
    path('clients/', clients, name='clients'),
    path('<int:pk>/client_update/', client_update, name='client_update'),
    path('<int:pk>/client_delete/', client_delete, name='client_delete'),
]
