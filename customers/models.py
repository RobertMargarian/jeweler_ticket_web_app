from django.db import models
from django.contrib.auth.models import AbstractUser



class Company(models.Model):
    company_current_plan = models.ForeignKey(("Plan"), null=True, blank=True, on_delete=models.CASCADE)
    company_subscription_status = models.CharField(choices=(('Active','Active'), ('Inactive','Inactive'), ('Cancelled', 'Cancelled')), max_length=30)
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
    CompanyOwner = 1
    CompanyAdmin = 2
    Employee = 3

    ROLE_CHOICES = (
        (CompanyOwner, 'CompanyOwner'),
        (CompanyAdmin, 'CompanyAdmin'),
        (Employee, 'Employee'),
    )

    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    user_phone = models.CharField(max_length=20)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name + " " + self.last_name + " | " + self.user_role.__str__()



"""     class Meta:
        permissions = (
            ("can_view_all_orders", "Can view all orders"),
            ("can_view_all_clients", "Can view all clients"),

        )   """  


""" class UserProfile(models.Model):
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " | " + self.user.first_name + " " + self.user.last_name """


class Order(models.Model):
    client = models.ForeignKey(("Client"), null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.SET_NULL)
    work_order_date = models.DateTimeField(auto_now_add=True)
    work_order_due_date = models.DateTimeField(max_length=50)
    estimated_cost = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    work_order_currency = models.CharField(choices=(('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')), max_length=10)
    quoted_price = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    quoted_currency = models.CharField(choices=(('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')), max_length=10)
    security_deposit = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    work_order_type = models.CharField(choices=(('Sell','Sell'), ('Repair','Repair'), ('Other', 'Other')), max_length=30)
    work_order_status = models.CharField(choices=(('Cancelled','Cancelled'), ('In Progress','In Progress'), ('Completed', 'Completed')), max_length=30)
    work_order_description = models.TextField(max_length=200)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company.company_name + " | " + self.client.client_first_name + " " + self.client.client_last_name

"""     def delete(self):
        self.deleted_flag = True
        self.save() """


class Client(models.Model):
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    client_already_exists = models.BooleanField(default=False)
    client_first_name = models.CharField(max_length=50)
    client_last_name = models.CharField(max_length=50)
    client_email = models.EmailField(max_length=254)
    client_phone = models.CharField(max_length=20)
    client_check_mobile_phone = models.BooleanField(default=False)
    total_spent = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_first_name + " " + self.client_last_name + " " 



""" class UserActivityLog(models.Model):
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
"""

""" class UserAction(models.Model):
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
    action_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + " " + self.action_name """


class BillingLog(models.Model):
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
    plan_trial_period = models.CharField(choices=(('Yes','Yes'), ('No','No')), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name


""" class SoftDeleteModel(models.Model):

    deleted_flag = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted_flag = True
        self.save()

    def restore(self):
        self.deleted_flag = False
        self.save()

    class Meta:
        abstract = True
"""

