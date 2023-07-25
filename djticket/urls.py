from django.contrib import admin
from django.urls import path

from customers.views import orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', orders)
]
