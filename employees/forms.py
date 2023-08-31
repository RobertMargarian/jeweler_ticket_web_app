from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from customers.models import Order, Company, Client, User


User = get_user_model()

class EmployeeModelForm(forms.ModelForm):
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

    