from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
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
        widget=forms.CheckboxSelectMultiple(),
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

    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=True)
    estimated_cost = forms.DecimalField(min_value=0.00, max_digits=10, decimal_places=2, initial=0, required=True)
    work_order_status = forms.ChoiceField(choices=order_status_choices, initial='In Progress', required=True)
    quoted_price = forms.DecimalField(min_value=0.00, max_value=1000000, max_digits=10, decimal_places=2, initial=0, required=True)
    security_deposit = forms.DecimalField(min_value=0.00, max_value=1000000, max_digits=10, decimal_places=2, initial=0, required=False)
    work_order_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    work_order_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)


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
            'work_order_description'
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(company=user.company)

    def clean(self):
        clean_data = super().clean()        
        quoted_price = self.cleaned_data.get('quoted_price')
        estimated_cost = self.cleaned_data.get('estimated_cost')
        security_deposit = self.cleaned_data.get('security_deposit')
        if quoted_price is not None and estimated_cost is not None and quoted_price < estimated_cost:
            self.add_error('quoted_price', "Quoted price cannot be less than estimated cost")

        if quoted_price is not None and security_deposit is not None and security_deposit > quoted_price:
            self.add_error('security_deposit', "Security deposit cannot be greater than quoted price")

