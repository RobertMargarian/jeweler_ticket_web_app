from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
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
        widget=forms.Select(attrs={'id': 'pagination'}),
        label="Orders per page"
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
            'work_order_description'
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(company=user.company)

