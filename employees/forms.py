from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from customers.models import Order, Company, Client, User


User = get_user_model()


class PaginationForm(forms.Form):
    page_size_choices = [
        (1, '1'),
        (2, '2'),
        (5, '5'),
        (100, '100')
    ]

    page_size = forms.ChoiceField(
        choices=page_size_choices,
        widget=forms.Select(attrs={'id': 'pagination_employees'}),
        label="Employees per page"
    )


class EmployeeModelForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=False)
    user_phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'user_phone',
            'password',
        ]

    