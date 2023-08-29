from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
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
        widget=forms.Select(attrs={'id': 'pagination_orders'}),
        label="Orders per page"
    )

class OrderCreateForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=True)
    estimated_cost = forms.DecimalField(min_value=0.00, max_digits=10, decimal_places=2, required=True)
    quoted_price = forms.DecimalField(min_value=0.00, max_digits=10, decimal_places=2, required=True)
    security_deposit = forms.DecimalField(min_value=0.00, max_digits=10, decimal_places=2, required=True)
    work_order_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    work_order_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)


    class Meta:
        model = Order
        fields = (
            'client',
            'work_order_type',
            'estimated_cost', 
            'quoted_price', 
            'security_deposit', 
            'work_order_due_date',
            'work_order_description'
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(company=user.company)

    # def clean_order_due_date(self):
    #     work_order_due_date = self.cleaned_data.get('work_order_due_date')
    #     created_at = self.instance.created_at
    #     if work_order_due_date < created_at:
    #         raise ValidationError("Due date cannot be in the past")
    #     return work_order_due_date 

    #     def clean_quoted_price(self):
    #     quoted_price = self.cleaned_data.get('quoted_price')
    #     estimated_cost = self.cleaned_data.get('estimated_cost')
    #     if quoted_price < estimated_cost:
    #         raise ValidationError("Quoted price cannot be less than estimated cost")
    #     return quoted_price
    
    # def clean_security_deposit(self):
    #     security_deposit = self.cleaned_data.get('security_deposit')
    #     quoted_price = self.cleaned_data.get('quoted_price')
    #     if security_deposit > quoted_price:
    #         raise ValidationError("Security deposit cannot be greater than quoted price")
    #     return security_deposit
    
