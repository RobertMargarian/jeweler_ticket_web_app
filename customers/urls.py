from django.urls import path
from .views import orders, order_detail


urlpatterns = [
    path('', orders),
    path('<int:pk>/', order_detail)
]
