from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    company_id = models.AutoField(("Company ID"), primary_key=True)
    company_current_plan_id = models.ForeignKey(("Plan ID"), on_delete=models.CASCADE)
    company_subscription_status = models.CharField(("Company Subscription Status"), max_length=50)
    company_email = models.EmailField(("Company Email"), max_length=254)
    company_phone = models.CharField(("Company Phone"), max_length=20)
    company_name = models.CharField(("Company Name"), max_length=50)
    owner_first_name = models.CharField(("Owner First Name"), max_length=50)
    owner_last_name = models.CharField(("Owner Last Name"), max_length=50)
    company_can_contact = models.BooleanField(("Company Can Contact"), default=False)
    company_can_email = models.BooleanField(("Company Can Email"), default=False)
    company_address_lines = models.TextField(("Company Address Lines"))
    company_city = models.CharField(("Company City"), max_length=50)
    company_state = models.CharField(("Company State"), max_length=50)
    company_country = models.CharField(("Company Country"), max_length=50)
    company_zip_code = models.CharField(("Company Zip Code"), max_length=50)
    first_sign_up_date = models.DateTimeField(("First Sign Up Date"), auto_now_add=True)
    last_sign_up_date = models.DateTimeField(("Last Sign Up Date"), auto_now_add=True)
    first_subscription_date = models.DateTimeField(("First Subscription Date"), auto_now_add=True)
    last_subscription_date = models.DateTimeField(("Last Subscription Date"), auto_now_add=True)
    first_cancelation_date = models.DateTimeField(("First Cancelation Date"), auto_now_add=True)
    last_cancelation_date = models.DateTimeField(("Last Cancelation Date"), auto_now_add=True)
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User(AbstractUser):
    user_id = models.BigIntegerField(("User ID"), primary_key=True)
    company_id = models.ForeignKey(("Company ID"), on_delete=models.CASCADE)
    role_id = models.ForeignKey(("Role ID"), on_delete=models.CASCADE)
    user_login = models.CharField(("User Login"), max_length=50)
    user_password = models.CharField(("User Password"), max_length=50)
    user_first_name = models.CharField(("User First Name"), max_length=50)
    user_last_name = models.CharField(("User Last Name"), max_length=50)
    user_email = models.EmailField(("User Email"), max_length=254)
    user_phone = models.CharField(("User Phone"), max_length=20)
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Order(models.Model):
    work_order_id = models.BigIntegerField(("Work Order ID"), primary_key=True)
    client_id = models.ForeignKey(("Client ID"), on_delete=models.CASCADE)
    company_id = models.ForeignKey(("Company ID"), on_delete=models.CASCADE)
    user_id = models.ForeignKey(("User ID"), on_delete=models.CASCADE)
    work_order_date = models.DateTimeField(("Work Order Date"), auto_now_add=True)
    work_order_due_date = models.DateTimeField(("Work Order Due Date"), auto_now_add=True)
    work_order_price = models.DecimalField(("Work Order Price"), max_digits=10, decimal_places=2, default=0.00)
    work_order_currency = models.CharField(("Work Order Currency"), max_length=10)
    quoted_price = models.DecimalField(("Quoted Price"), max_digits=10, decimal_places=2, default=0.00)
    quoted_currency = models.CharField(("Quoted Currency"), max_length=10)
    work_order_type = models.CharField(("Work Order Type"), max_length=50)
    work_order_status = models.CharField(("Work Order Status"), max_length=50)
    work_order_description = models.TextField(("Work Order Description"))
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Client(models.Model):
    client_id = models.BigIntegerField(("Client ID"), primary_key=True)
    company_id = models.ForeignKey(("Company ID"), on_delete=models.CASCADE)
    client_email = models.EmailField(("Client Email"), max_length=254)
    client_phone = models.CharField(("Client Phone"), max_length=20)
    client_first_name = models.CharField(("Client First Name"), max_length=50)
    client_last_name = models.CharField(("Client Last Name"), max_length=50)
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User_Role(models.Model):
    user_role_id = models.BigIntegerField(("User Role ID"), primary_key=True)
    user_role_name = models.CharField(("User Role Name"), max_length=50)
    user_role_description = models.TextField(("User Role Description"))
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User_Activity_Log(models.Model):
    user_activity_log_id = models.BigIntegerField(("User Activity Log ID"), primary_key=True)
    user_id = models.ForeignKey(("User ID"), on_delete=models.CASCADE)
    user_action_id = models.ForeignKey(("User Action ID"), on_delete=models.CASCADE)
    work_order_id = models.ForeignKey(("Work Order ID"), on_delete=models.CASCADE)
    client_id = models.ForeignKey(("Client ID"), on_delete=models.CASCADE)
    user_activity_time = models.DateTimeField(("User Activity Time"), auto_now_add=True)
    deleted_flag = models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)

class User_Action(models.Model):
    action_id = models.BigIntegerField(("Action ID"), primary_key=True)
    action_name = models.CharField(("Action Name"), max_length=50)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Billing_Log(models.Model):
    company_id = models.BigIntegerField(("Company ID"), primary_key=True)
    plan_id = models.ForeignKey(("Plan ID"), on_delete=models.CASCADE)
    billing_date = models.DateTimeField(("Billing Date"), auto_now_add=True)
    billing_amount = models.DecimalField(("Billing Amount"), max_digits=10, decimal_places=2)
    billing_status = models.CharField(("Billing Status"), max_length=50)
    billing_period_start_date = models.DateTimeField(("Billing Period Start Date"), auto_now_add=True)
    billing_period_end_date = models.DateTimeField(("Billing Period End Date"), auto_now_add=True)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Plan(models.Model):
    plan_id = models.BigIntegerField(("Plan ID"), primary_key=True)
    plan_name = models.CharField(("Plan Name"), max_length=50)
    plan_frequency = models.CharField(("Plan Frequency"), max_length=50)
    plan_price = models.DecimalField(("Plan Price"), max_digits=10, decimal_places=2)
    plan_currency = models.CharField(("Plan Currency"), max_length=50)
    plan_description = models.TextField(("Plan Description"))
    plan_features = models.TextField(("Plan Features"))
    plan_trial_period = models.CharField(("Plan Trial Period"), max_length=50)
    created_at = models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.DateTimeField(("Ingestion Timestamp"), auto_now=True)

