from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Client, Company, User

User = get_user_model()


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'client_first_name',
            'client_last_name',
            'client_email',
            'client_phone',
            'client_check_mobile_phone',
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'user_phone',
        )
        field_classes = {
            'username': UsernameField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'email': forms.EmailField,
            'user_phone': forms.CharField,
        }


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'company_name',
            'company_address_lines',
            'company_city',
            'company_state',
            'company_country',
            'company_zip_code',
            'company_phone',
            'company_email',
        )
        field_classes = {
            'company_name': forms.CharField,
            'company_address_lines': forms.CharField,
            'company_city': forms.CharField,
            'company_state': forms.CharField,
            'company_country': forms.CharField,
            'company_zip_code': forms.CharField,
            'company_phone': forms.CharField,
            'company_email': forms.EmailField,
        }
