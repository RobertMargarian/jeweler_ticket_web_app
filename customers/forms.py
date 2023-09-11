from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Client, Company, User, Order
from orders.forms import OrderCreateForm


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
        widget=forms.Select(attrs={'id': 'pagination_clients'}),
        label="Clients per page"
    )


class ClientCreateForm(forms.ModelForm):
    client_already_exists = forms.BooleanField(
        label='Existing Client?', 
        required=False, 
        initial=False,
        widget=forms.Select(
            choices=[
                (True, 'Yes'),
                (False, 'No')
            ],
            attrs={'class': 'form-control'}
        )
    )

    client_first_name = forms.CharField(label='Client First Name', max_length=50, required=False, initial=None, widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_last_name = forms.CharField(label='Client Last Name', max_length=50, required=False, initial=None, widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_email = forms.EmailField(label='Client Email Address', max_length=254, required=False, initial=None, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    client_phone = forms.CharField(label='Client Phone Number', max_length=20, required=False, initial=None, widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_check_mobile_phone = forms.BooleanField(label='Is this mobile phone?', required=False, initial=False)


    class Meta:
        model = Client
        fields = (
            'client_already_exists',
            'client_first_name',
            'client_last_name',
            'client_email',
            'client_phone',
            'client_check_mobile_phone',
        )

    def clean(self):
        cleaned_data = super().clean()
        client_already_exists = cleaned_data.get("client_already_exists")
        client_first_name = cleaned_data.get("client_first_name")
        client_last_name = cleaned_data.get("client_last_name")
        client_phone = cleaned_data.get("client_phone")

        if client_already_exists == False:
            if client_first_name == None:
                self.add_error('client_first_name', "This field is required.")
            if client_last_name == None:
                self.add_error('client_last_name', "This field is required.")
            if client_phone == None:
                self.add_error('client_phone', "This field is required.")

        return cleaned_data
    
    
# class CombinedCreateForm(forms.Form):
#     def __init__(self, user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         user = User.objects.get(username=user)
#         self.fields['client_form'] = ClientCreateForm()
#         self.fields['order_form'] = OrderCreateForm(user=user)




    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     if 'client_already_exists' == True:
    #         self.fields['client_first_name'].required = False
    #         self.fields['client_last_name'].required = False
    #         self.fields['client_email'].required = False
    #         self.fields['client_phone'].required = False
    #     else:
    #         self.fields['client_first_name'].required = True
    #         self.fields['client_last_name'].required = True
    #         self.fields['client_email'].required = True
    #         self.fields['client_phone'].required = True

        # widgets = {
        #     'client_first_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'client_last_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'client_email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'client_phone': forms.TextInput(attrs={'class': 'form-control'}),
        #     'client_check_mobile_phone': forms.CheckboxInput(attrs={'class': 'form-control'}),
        # }

        # field_classes = {
        #     'client_already_exists': forms.BooleanField,
        #     'client_first_name': forms.CharField,
        #     'client_last_name': forms.CharField,
        #     'client_email': forms.EmailField,
        #     'client_phone': forms.CharField,
        #     'client_check_mobile_phone': forms.BooleanField,
        # }







class CustomUserCreationForm(UserCreationForm):
    username = UsernameField(
        label='Username',
        max_length=150,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=False)
    user_phone = forms.CharField(max_length=20, required=True)


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'user_phone',
        )
        field_classes = {
            'username': UsernameField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'email': forms.EmailField,
            'user_phone': forms.CharField,
        }



class CompanyCreateForm(forms.ModelForm):
    company_name = forms.CharField(max_length=50, required=True)
    company_address_lines = forms.CharField(max_length=50, required=True)
    company_city = forms.CharField(max_length=50, required=True)
    company_state = forms.CharField(max_length=50, required=True)
    company_country = forms.CharField(max_length=50, required=True)
    company_zip_code = forms.CharField(max_length=50, required=True)
    company_phone = forms.CharField(max_length=20, required=True)
    company_email = forms.EmailField(max_length=254, required=True)


    class Meta:
        model = Company
        fields = (
            'company_name',
            'company_address_lines',
            'company_city',
            'company_state',
            'company_country',
            'company_zip_code',
            'company_phone',
            'company_email',
        )
        field_classes = {
            'company_name': forms.CharField,
            'company_address_lines': forms.CharField,
            'company_city': forms.CharField,
            'company_state': forms.CharField,
            'company_country': forms.CharField,
            'company_zip_code': forms.CharField,
            'company_phone': forms.CharField,
            'company_email': forms.EmailField,
        }
