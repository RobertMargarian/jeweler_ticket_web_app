from typing import Any
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, render, redirect, get_object_or_404
from .forms import EmployeeModelForm, PaginationForm
from customers.models import Client, Company, Employee, User


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'employees/employee_list.html'
    context_object_name = 'employee_list'

    def get_paginate_by(self, queryset):
        return self.request.user.pref_employees_per_page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form with the user's preference
        context['pagination_form_employee'] = \
            PaginationForm(initial={'page_size': self.request.user.pref_employees_per_page})
        
        context['employees_per_page'] = self.request.user.pref_employees_per_page
        return context

    def get_queryset(self):
        user = self.request.user
        company = self.request.user.company
        if user.is_owner:
            queryset = Employee.objects \
                .filter(user__is_active=True) \
                .filter(company=company)
            queryset = queryset.order_by('user__created_at')
        else:
            return KeyError("User does not have permission to view employees")
        return queryset
    
    def get(self, request, *args, **kwargs):
        # Check if page_size is being updated
        if 'page_size' in request.GET:
            try:
                page_size = request.GET.get('page_size')
                # Update the user's preference in the model
                request.user.pref_employees_per_page = page_size
                request.user.save()
            except ValueError:
                pass
        return super().get(request, *args, **kwargs)    
    

class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'employees/employee_create.html'
    form_class = EmployeeModelForm

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def get_queryset(self):
        company = self.request.user.company
        user = self.request.user
        if user.is_owner:
            queryset = Employee.objects.filter(company=company)
            queryset = queryset.filter(company=self.request.user.company)
        else:
            return KeyError("User does not have permission to create employees")
        return queryset

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_employee = True
        user.is_owner = False
        user.company = self.request.user.company
        user.set_password(form.cleaned_data['password'])

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
    context_object_name = 'employee-update'

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def get_queryset(self):
        company = self.request.user.company
        user = self.request.user
        if user.is_owner:
            queryset = Employee.objects \
                .filter(user__is_active=True) \
                .filter(company=company)
            queryset = queryset.filter(company=self.request.user.company)
        else:
            return KeyError("User does not have permission to view employees")
        return queryset
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        employee = self.get_object()
        kwargs['instance'] = employee.user
        return kwargs

class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'employees/employee_delete.html'
    context_object_name = 'employee-delete'
    model = Employee

    def get_success_url(self):
        return reverse('employees:employee-list')
    
    def get_queryset(self):
        company = self.request.user.company
        user = self.request.user
        if user.is_owner:
            queryset = Employee.objects.filter(company=company)
            queryset = queryset.filter(company=self.request.user.company)
        else:
            return KeyError("User does not have permission to view employees")
        return queryset
