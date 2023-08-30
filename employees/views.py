from typing import Any
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from .forms import EmployeeModelForm
from customers.models import Client, Company, Employee, User


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employee_list'

    def get_queryset(self):
        company = self.request.user.company
        return Employee.objects.filter(company=company)
    

class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'employees/employee_create.html'
    form_class = EmployeeModelForm

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_employee = True
        user.is_owner = False
        user.company = self.request.user.company
        user.save()
        Employee.objects.create(
            user=user,
            company=self.request.user.company
        )
        send_mail(
            subject="You are invited to be an employee",
            message="You were added as an employee on DJTICKET. Please login to your account to start working.",
            from_email="rgts@gmail.com",
            recipient_list=[user.email],
        )
        return super(EmployeeCreateView, self).form_valid(form)
    

class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'employees/employee_update.html'
    form_class = EmployeeModelForm

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def get_queryset(self):
        company = self.request.user.company
        return Employee.objects.filter(company=company)
    

class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'employees/employee_delete.html'
    context_object_name = 'employee'

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def get_queryset(self):
        company = self.request.user.company
        return Employee.objects.filter(company=company)
