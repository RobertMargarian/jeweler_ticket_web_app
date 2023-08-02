from django.urls import path
from .views import order_list, order_update, order_create, client_create, order_delete, client_list, client_update, client_delete


urlpatterns = [
    path('', order_list, name='order-list'),
    path('<int:pk>/order_update/', order_update, name='order-update'),
    path('<int:pk>/order_delete/', order_delete, name='order-delete'),
    path('order_create/', order_create, name='order-create'),
    path('client_create/', client_create, name='client-create'),
    path('client_list/', client_list, name='client-list'),
    path('<int:pk>/client_update/', client_update, name='client-update'),
    path('<int:pk>/client_delete/', client_delete, name='client-delete'),
]
