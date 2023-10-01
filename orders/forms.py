from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.forms.widgets import CheckboxSelectMultiple, Select
from django.forms import ModelForm
from django.core.validators import MinValueValidator
from customers.models import Order, Company, Client, User

User = get_user_model()


class OrderStatusFilterForm(forms.Form):
    order_status_choices = [
        ('Cancelled','Cancelled'),
        ('In Progress','In Progress'),
        ('Completed', 'Completed')
    ]

    order_status = forms.MultipleChoiceField(
        choices=order_status_choices,
        required=False,
        widget=forms.SelectMultiple(),  # Display 3 options at once
        label="Order Status"
    )

class PaginationForm(forms.Form):
    page_size_choices = [
        (1, '1'),
        (2, '2'),
        (5, '5'),
        (100, '100')
    ]

    page_size = forms.ChoiceField(
        choices=page_size_choices,
        widget=forms.Select(attrs={'id': 'pagination_orders'}),
        label="Orders per page"
    )

class OrderCreateForm(forms.ModelForm):
    order_status_choices = [
        ('Cancelled','Cancelled'),
        ('In Progress','In Progress'),
        ('Completed', 'Completed')
    ]

    order_type_choices = [
        ('Sell','Sell'),
        ('Repair','Repair'),
        ('Other', 'Other')
    ]

    client = forms.ModelChoiceField(label='Client', queryset=Client.objects.all(), required=False, initial=None, widget=forms.Select(attrs={'class': 'form-control'}))
    estimated_cost = forms.DecimalField(label='Estimated Cost', min_value=0.00, max_digits=10, decimal_places=2, initial=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    work_order_type = forms.ChoiceField(label='Order Type', choices=order_type_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    work_order_status = forms.ChoiceField(label='Status', choices=order_status_choices, initial='In Progress', required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    quoted_price = forms.DecimalField(label='Quoted Price', min_value=0.00, max_value=1000000, max_digits=10, decimal_places=2, initial=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    security_deposit = forms.DecimalField(label='Security Deposit', min_value=0.00, max_value=1000000, max_digits=10, decimal_places=2, initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    work_order_due_date = forms.DateField(label='Due Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    work_order_description = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    order_photo = forms.ImageField(
        label='Add Picture', 
        required=False, 
        widget=forms.FileInput(attrs={'accept': 'image/*', 'capture': 'camera'})
    )

    
    class Meta:
        model = Order
        fields = (
            'client',
            'work_order_type',
            'work_order_status',
            'estimated_cost', 
            'quoted_price', 
            'security_deposit', 
            'work_order_due_date',
            'work_order_description',
            'order_photo',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)

    def get_queryset(self):
        user = self.user
        self.fields['client'].queryset = Client.objects \
        .filter(company=user.company) \
        .filter(deleted_flag=False)
        return self.fields['client'].queryset


    def clean(self):
        cleaned_data = super().clean()
        quoted_price = self.cleaned_data.get('quoted_price')
        estimated_cost = self.cleaned_data.get('estimated_cost')
        security_deposit = self.cleaned_data.get('security_deposit')
        
        if quoted_price is not None and estimated_cost is not None and quoted_price < estimated_cost:
            self.add_error('quoted_price', "Quoted price cannot be less than estimated cost")

        if quoted_price is not None and security_deposit is not None and security_deposit > quoted_price:
            self.add_error('security_deposit', "Security deposit cannot be greater than quoted price")

        return cleaned_data

