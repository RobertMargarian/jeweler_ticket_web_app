from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Order, Client

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


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'client',
            'work_order_type',
            'estimated_cost', 
            'quoted_price', 
            'security_deposit', 
            'work_order_due_date',
            'work_order_status',
            'work_order_description'
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
            'user_role',
        )
        field_classes = {
            'username': UsernameField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'email': forms.EmailField,
            'user_phone': forms.CharField,
            'user_role': forms.ChoiceField,
        }


""" class ClientCheckForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'client_already_exists',
        ) """


""" class OrderForm(forms.Form):
    client_first_name = forms.CharField(max_length=100)
    client_last_name = forms.CharField(max_length=100)
    client_email = forms.EmailField()
    client_phone = forms.CharField(max_length=20)
    client_check_mobile_phone = forms.BooleanField(required=False)
    work_order_date = forms.DateField()
    work_order_due_date = forms.DateField()
    estimated_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    quoted_price = forms.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = forms.DecimalField(max_digits=10, decimal_places=2)
    work_order_type = forms.ChoiceField(choices=(('Sell','Sell'), ('Repair','Repair'), ('Other', 'Other')))
    work_order_status = forms.ChoiceField(choices=(('Canceled','Canceled'), ('In Progress','In Progress'), ('Completed', 'Completed')))
"""

"""     new_client = forms.BooleanField(required=False)
    client = forms.ModelChoiceField(queryset=Client.objects.all()) """