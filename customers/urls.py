from django.urls import path
from .views import orders, order_detail


urlpatterns = [
    path('', orders),
    path('<pk>/', order_detail)
]
