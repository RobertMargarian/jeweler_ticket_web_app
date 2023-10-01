# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, UsernameField
# from django.core.exceptions import ValidationError
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
# from django.forms.widgets import CheckboxSelectMultiple, Select
# from django.forms import ModelForm
# from django.core.validators import MinValueValidator
# from customers.models import Order, Company, Client, User

# User = get_user_model()


# class CompanyDetailForm(forms.Form):
#     class Meta:


#         model = Company
#         fields = (
#             'company_name',
#             'company_phone',
#             'company_email',
#             'company_address_lines',
#             'company_city',
#             'company_state',
#             'company_zip_code',
#             'company_country',
#         )

#         widgets = {
#             'company_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_email': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_address_lines': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_city': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_state': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_zip_code': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_country': forms.TextInput(attrs={'class': 'form-control'}),
#         }