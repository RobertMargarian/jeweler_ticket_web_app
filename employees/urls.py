from django.urls import path
from .views import (
    EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView
)

app_name = 'employees'

urlpatterns = [
    path('employee_list/', EmployeeListView.as_view(), name='employee-list'),
    path('employee_create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:pk>/employee_update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/employee_delete/', EmployeeDeleteView.as_view(), name='employee-delete'),    
]