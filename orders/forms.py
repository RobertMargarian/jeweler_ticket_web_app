from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from customers.models import Order

User = get_user_model()

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
