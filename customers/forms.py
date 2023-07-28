from django import forms
from .models import Order, Client


class OrderForm(forms.Form):
    client_first_name = forms.CharField(max_length=100)
    client_last_name = forms.CharField(max_length=100)
    client_email = forms.EmailField()
    client_phone = forms.CharField(max_length=20)
    client_check_mobile_phone = forms.BooleanField(required=False)
    work_order_date = forms.DateField()
    work_order_due_date = forms.DateField()
    estimated_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    add_to_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    quoted_price = forms.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = forms.DecimalField(max_digits=10, decimal_places=2)
    work_order_type = forms.ChoiceField(choices=(('Sell','Sell'), ('Repair','Repair'), ('Other', 'Other')))
    work_order_status = forms.ChoiceField(choices=(('Canceled','Canceled'), ('In Progress','In Progress'), ('Completed', 'Completed')))


"""     new_client = forms.BooleanField(required=False)
    client = forms.ModelChoiceField(queryset=Client.objects.all()) """