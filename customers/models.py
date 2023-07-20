from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(("User ID"), primary_key=True)
    company_id = models.BigIntegerField(("Company ID"), foreign_key=True)
    role_id = models.BigIntegerField(("Role ID"), foreign_key=True)
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
    client_id = models.BigIntegerField(("Client ID"), foreign_key=True)
    company_id = models.BigIntegerField(("Company ID"), foreign_key=True)
    user_id = models.BigIntegerField(("User ID"), foreign_key=True)
    work_order_date = models.DateTimeField(("Work Order Date"), auto_now_add=True)
    work_order_due_date = models.DateTimeField(("Work Order Due Date"), auto_now_add=True)
    work_order_price = models.DecimalField(("Work Order Price"), max_digits=10, decimal_places=2, default=0.00)
    work_order_currency = models.CharField(("Work Order Currency"), max_length=10)
    quoted_price = models.DecimalField(("Quoted Price"), max_digits=10, decimal_places=2, default=0.00)
    quoted_currency = models.CharField(("Quoted Currency"), max_length=10)
    work_order_type = models.CharField(("Work Order Type"), max_length=50)
    work_order_status = models.CharField(("Work Order Status"), max_length=50)
    work_order_description = models.TextField(("Work Order Description"))
    deleted_flag = models.models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Client(models.Model):
    client_id = models.models.BigIntegerField(("Client ID"), primary_key=True)
    company_id = models.models.BigIntegerField(("Company ID"), foreign_key=True)
    client_email = models.models.EmailField(("Client Email"), max_length=254)
    client_phone = models.models.CharField(("Client Phone"), max_length=20)
    client_first_name = models.models.CharField(("Client First Name"), max_length=50)
    client_last_name = models.models.CharField(("Client Last Name"), max_length=50)
    deleted_flag = models.models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Company(models.Model):
    company_id = models.models.BigIntegerField(("Company ID"), primary_key=True)
    company_plan_id = models.models.BigIntegerField(("Company Plan ID"), foreign_key=True)
    company_subscription_status = models.models.CharField(("Company Subscription Status"), max_length=50)
    company_email = models.models.EmailField(("Company Email"), max_length=254)
    company_phone = models.models.CharField(("Company Phone"), max_length=20)
    company_name = models.models.CharField(("Company Name"), max_length=50)
    owner_first_name = models.models.CharField(("Owner First Name"), max_length=50)
    owner_last_name = models.models.CharField(("Owner Last Name"), max_length=50)
    company_can_contact = models.models.BooleanField(("Company Can Contact"), default=False)
    company_can_email = models.models.BooleanField(("Company Can Email"), default=False)
    company_address_lines = models.models.TextField(("Company Address Lines"))
    company_city = models.models.CharField(("Company City"), max_length=50)
    company_state = models.models.CharField(("Company State"), max_length=50)
    company_country = models.models.CharField(("Company Country"), max_length=50)
    company_zip_code = models.models.CharField(("Company Zip Code"), max_length=50)
    first_sign_up_date = models.models.DateTimeField(("First Sign Up Date"), auto_now_add=True)
    last_sign_up_date = models.models.DateTimeField(("Last Sign Up Date"), auto_now_add=True)
    first_subscription_date = models.models.DateTimeField(("First Subscription Date"), auto_now_add=True)
    last_subscription_date = models.models.DateTimeField(("Last Subscription Date"), auto_now_add=True)
    first_cancelation_date = models.models.DateTimeField(("First Cancelation Date"), auto_now_add=True)
    last_cancelation_date = models.models.DateTimeField(("Last Cancelation Date"), auto_now_add=True)
    deleted_flag = models.models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User_Role(models.Model):
    user_role_id = models.BigIntegerField(("User Role ID"), primary_key=True)
    user_role_name = models.CharField(("User Role Name"), max_length=50)
    user_role_description = models.TextField(("User Role Description"))
    deleted_flag = models.models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User_Activity_Log(models.Model):
    user_activity_log_id = models.BigIntegerField(("User Activity Log ID"), primary_key=True)
    user_id = models.BigIntegerField(("User ID"), foreign_key=True)
    user_action_id = models.BigIntegerField(("User Action ID"), foreign_key=True)
    work_order_id = models.BigIntegerField(("Work Order ID"), foreign_key=True)
    client_id = models.BigIntegerField(("Client ID"), foreign_key=True)
    user_activity_time = models.DateTimeField(("User Activity Time"), auto_now_add=True)
    deleted_flag = models.models.BooleanField(("Deleted Flag"), default=False)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class User_Action(models.Model):
    action_id = models.BigIntegerField(("Action ID"), primary_key=True)
    action_name = models.CharField(("Action Name"), max_length=50)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Billing_Log(models.Model):
    company_id = models.BigIntegerField(("Company ID"), primary_key=True)
    plan_id = models.BigIntegerField(("Plan ID"), foreign_key=True)
    billing_date = models.DateTimeField(("Billing Date"), auto_now_add=True)
    billing_amount = models.models.DecimalField(("Billing Amount"), max_digits=10, decimal_places=2)
    billing_status = models.models.CharField(("Billing Status"), max_length=50)
    billing_period_start_date = models.DateTimeField(("Billing Period Start Date"), auto_now_add=True)
    billing_period_end_date = models.DateTimeField(("Billing Period End Date"), auto_now_add=True)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)


class Plan(models.Model):
    plan_id = models.BigIntegerField(("Plan ID"), primary_key=True)
    plan_name = models.CharField(("Plan Name"), max_length=50)
    plan_frequency = models.models.CharField(("Plan Frequency"), max_length=50)
    plan_price = models.models.DecimalField(("Plan Price"), max_digits=10, decimal_places=2)
    plan_currency = models.models.CharField(("Plan Currency"), max_length=50)
    plan_description = models.TextField(("Plan Description"))
    plan_features = models.TextField(("Plan Features"))
    plan_trial_period = models.models.CharField(("Plan Trial Period"), max_length=50)
    created_at = models.models.DateTimeField(("Created At"), auto_now_add=True)
    updated_at = models.models.DateTimeField(("Updated At"), auto_now=True)
    ingestion_timestamp = models.models.DateTimeField(("Ingestion Timestamp"), auto_now=True)

