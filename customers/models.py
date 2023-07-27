from django.db import models
from django.contrib.auth.models import AbstractUser



class Company(models.Model):
    company_current_plan = models.ForeignKey(("Plan"), null=True, blank=True, on_delete=models.CASCADE)
    company_subscription_status = models.CharField(choices=(('Active','Active'), ('Inactive','Inactive'), ('Canceled', 'Canceled')), max_length=30)
    company_email = models.EmailField(max_length=254)
    company_phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    company_can_contact = models.BooleanField(default=False)
    company_can_email = models.BooleanField(default=False)
    company_address_lines = models.TextField(max_length=200)
    company_city = models.CharField(max_length=50)
    company_state = models.CharField(max_length=50)
    company_country = models.CharField(max_length=50)
    company_zip_code = models.CharField(max_length=50)
    first_sign_up_date = models.DateTimeField(auto_now_add=True)
    last_sign_up_date = models.DateTimeField(auto_now_add=True)
    first_subscription_date = models.DateTimeField(auto_now_add=True)
    last_subscription_date = models.DateTimeField(auto_now_add=True)
    first_cancelation_date = models.DateTimeField(auto_now_add=True)
    last_cancelation_date = models.DateTimeField(auto_now_add=True)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class User(AbstractUser):
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey(("User_Role"), null=True, blank=True, on_delete=models.CASCADE)
    user_phone = models.CharField(max_length=20)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Order(models.Model):
    client = models.ForeignKey(("Client"), null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
    work_order_date = models.DateTimeField(auto_now_add=True)
    work_order_due_date = models.DateTimeField(auto_now_add=True)
    work_order_price = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    work_order_currency = models.CharField(choices=(('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')), max_length=10)
    quoted_price = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    quoted_currency = models.CharField(choices=(('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')), max_length=10)
    work_order_type = models.CharField(choices=(('Sell','Sell'), ('Repair','Repair'), ('Other', 'Other')), max_length=30)
    work_order_status = models.CharField(choices=(('Canceled','Canceled'), ('In Progress','In Progress'), ('Completed', 'Completed')), max_length=30)
    work_order_description = models.TextField(max_length=200)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client + " " + self.work_order_type + " " + self.work_order_status
    

class Client(models.Model):
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    client_email = models.EmailField(max_length=254)
    client_phone = models.CharField(max_length=20)
    client_first_name = models.CharField(max_length=50)
    client_last_name = models.CharField(max_length=50)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_first_name + " " + self.client_last_name


class User_Role(models.Model):
    user_role_name = models.CharField(choices=(('Owner','Owner'), ('Manager','Manager'), ('Employee', 'Employee')), max_length=30)
    user_role_description = models.TextField(max_length=200)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_role_name


class User_Activity_Log(models.Model):
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
    user_action = models.ForeignKey(("User_Action"), null=True, blank=True, on_delete=models.CASCADE)
    work_order = models.ForeignKey(("Order"), null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(("Client"), null=True, blank=True, on_delete=models.CASCADE)
    user_activity_time = models.DateTimeField(auto_now_add=True)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + " " + self.user_action + " " + self.user_activity_time


class User_Action(models.Model):
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
    action_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + " " + self.action_name


class Billing_Log(models.Model):
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(("Plan"), null=True, blank=True, on_delete=models.CASCADE)
    billing_date = models.DateTimeField(auto_now_add=True)
    billing_amount = models.DecimalField(max_digits=100000000000, decimal_places=2)
    billing_status = models.CharField(choices=(('Paid','Paid'), ('Unpaid','Unpaid'), ('Canceled', 'Canceled')), max_length=30)
    billing_period_start_date = models.DateTimeField(auto_now_add=True)
    billing_period_end_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company + " " + self.billing_status


class Plan(models.Model):
    plan_name = models.CharField(choices=(('Basic','Basic'), ('Standard','Standard'), ('Premium', 'Premium')), max_length=30)
    plan_frequency = models.CharField(max_length=50)
    plan_price = models.DecimalField(max_digits=100000000000, decimal_places=2)
    plan_currency = models.CharField(choices=(('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')), max_length=10)
    plan_description = models.TextField(max_length=200)
    plan_features = models.TextField(max_length=200)
    plan_trial_period = models.CharField(choices=(('Yes','Yes'), ('No','No')), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name

