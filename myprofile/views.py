from typing import Any, Dict
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, render, redirect
from django.views import generic
from customers.models import Company, User
from django.forms import modelformset_factory, formset_factory
from customers.forms import CompanyCreateForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic


class MyProfileView(LoginRequiredMixin, generic.ListView):
    template_name = "myprofile/myprofile.html"
    context_object_name = "myprofile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['subscription_status'] = self.request.user.company.company_subscription_status
        context['current_plan'] = self.request.user.company.company_current_plan
        return context
    
    def get_queryset(self):
        user = self.request.user
        if user.is_owner:
            queryset = User.objects \
                .filter(company=user.company)
        else:
            return KeyError("User does not have permission to view orders")
        return queryset
    

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "myprofile/user_detail.html"
    context_object_name = "user-detail"

    def get_queryset(self):
        queryset = User.objects \
            .filter(id=self.request.user.id)
        return queryset
    
    def get_success_url(self):
        return reverse("myprofile:myprofile")
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['subscription_status'] = self.request.user.company.company_subscription_status
        context['current_plan'] = self.request.user.company.company_current_plan
        return context
    

class CompanyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Company
    form_class = CompanyCreateForm
    template_name = "myprofile/company_detail.html"
    context_object_name = "company-detail"
    
    def get_success_url(self):
        return reverse("myprofile:myprofile")

    def get_queryset(self):
        queryset = Company.objects \
            .filter(id=self.request.user.company.id)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['subscription_status'] = self.request.user.company.company_subscription_status
        context['current_plan'] = self.request.user.company.company_current_plan
        return context





class SubscriptionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Company
    template_name = "myprofile/subscription_detail.html"
    context_object_name = "subscription-detail"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        return context
    
    def get_queryset(self):
        queryset = Company.objects \
            .filter(id=self.request.user.company.id)
        return queryset
    
    def get_success_url(self):
        return reverse("myprofile:myprofile")
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())
    


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "myprofile/user_update.html"
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    context_object_name = "user-update"
    
    def get_success_url(self):
        return reverse("myprofile:myprofile")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_owner:
            queryset = User.objects \
                .filter(company=user.company) \
                # .filter(deleted_flag=False)
        else:
            return KeyError("User does not have permission to view orders")
        return queryset
    
    def form_valid(self, form):
        user = self.request.user
        return super().form_valid(form)