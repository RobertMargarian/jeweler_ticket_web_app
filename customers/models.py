from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from io import BytesIO
import os



class Company(models.Model):
    COMPANY_SUBSCRIPTION_STATUS_CHOICES = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Cancelled', 'Cancelled'),
    )

    company_current_plan = models.ForeignKey(("Plan"), null=True, blank=True, on_delete=models.CASCADE)
    company_subscription_status = models.CharField(choices=COMPANY_SUBSCRIPTION_STATUS_CHOICES, max_length=30)
    # company_email = models.EmailField(max_length=254)
    # company_phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    company_can_contact = models.BooleanField(default=False)
    company_can_email = models.BooleanField(default=False)
    company_address_lines = models.TextField(max_length=200)
    company_city = models.CharField(max_length=50)
    company_state = models.CharField(max_length=50)
    # company_country = models.CharField(max_length=50)
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
    # is_owner = 1
    # is_admin = 2
    # is_employee = 3

    # ROLE_CHOICES = (
    #     (is_owner, 'is_owner'),
    #     (is_admin, 'is_admin'),
    #     (is_employee, 'is_employee'),
    # )

    is_owner = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    # user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    
    user_phone = models.CharField(max_length=20)
    # deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)
    pref_clients_per_page = models.PositiveSmallIntegerField(default=10)
    pref_orders_per_page = models.PositiveSmallIntegerField(default=2)
    pref_employees_per_page = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.first_name + " " + self.last_name + " | " + self.username
    

class Employee(models.Model):
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.company.company_name

    def delete(self, using=None, keep_parents=False):
        self.user.is_active = False
        self.user.save()


class Owner(models.Model):
    user = models.OneToOneField(("User"), null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.company.company_name

    def delete(self, using=None, keep_parents=False):
        self.user.is_active = False
        self.user.save()


class Order(models.Model):
    WORK_ORDER_STATUS_CHOICES = (
        ('Cancelled','Cancelled'),
        ('In Progress','In Progress'),
        ('Completed', 'Completed'),
    )

    WORK_ORDER_TYPE_CHOICES = (
        ('Sell','Sell'),
        ('Repair','Repair'),
        ('Other', 'Other'),
    )

    WORK_ORDER_CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    )


    client = models.ForeignKey(("Client"), null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.SET_NULL)
    work_order_date = models.DateField(default=timezone.now)
    work_order_due_date = models.DateField(default=timezone.now)

    estimated_cost = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    work_order_currency = models.CharField(choices=WORK_ORDER_CURRENCY_CHOICES, max_length=10)
    quoted_price = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    quoted_currency = models.CharField(choices=WORK_ORDER_CURRENCY_CHOICES, max_length=10)
    security_deposit = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    work_order_type = models.CharField(choices=WORK_ORDER_TYPE_CHOICES, max_length=30)
    work_order_status = models.CharField(default="In Progress", choices=WORK_ORDER_STATUS_CHOICES, max_length=30)
    work_order_description = models.TextField(max_length=200, default=None, null=True, blank=True)
    order_photo = models.ImageField(upload_to='order_photos/', blank=True, null=True)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

        # Check if an image has been uploaded
        if self.order_photo:
            img = Image.open(self.order_photo.path)
            
            # Define the maximum file size you want in bytes (e.g., 300 KB)
            max_file_size = 300 * 1024  # 300 KB in bytes

            # Create a BytesIO buffer for image compression
            img_io = BytesIO()

            # Compress the image while it's larger than the desired file size
            quality = 90  # Adjust this quality as needed (higher values result in lower quality)
            img.save(img_io, format='JPEG', quality=quality)
            while img_io.tell() > max_file_size and quality >= 10:
                # Reduce image quality if it's larger than the desired file size
                img_io.truncate(0)
                img_io.seek(0)
                quality -= 10
                img.save(img_io, format='JPEG', quality=quality)

            # Save the compressed image back to the same path
            with open(self.order_photo.path, 'wb') as f:
                f.write(img_io.getvalue())

    def __str__(self):
        return str(self.id) + " | " + self.company.company_name + " | " + self.work_order_status + " | " + self.work_order_type

    def delete(self, using=None, keep_parents=False):
        self.deleted_flag = True
        self.save()


class Client(models.Model):
    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.SET_NULL)
    client_already_exists = models.BooleanField(default=False)
    client_first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    client_last_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    client_email = models.EmailField(max_length=254, default=None, null=True, blank=True)
    client_phone = models.CharField(max_length=20, default=None, null=True, blank=True)
    client_check_mobile_phone = models.BooleanField(default=False, null=True, blank=True)
    total_spent = models.DecimalField(max_digits=1000000000, decimal_places=2, default=0.00)
    deleted_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_first_name + " " + self.client_last_name

    def delete(self):
        self.deleted_flag = True
        self.save()

        self.order_set.all().update(deleted_flag=True)


# class UserActivityLog(models.Model):
#     user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
#     user_action = models.ForeignKey(("User_Action"), null=True, blank=True, on_delete=models.CASCADE)
#     work_order = models.ForeignKey(("Order"), null=True, blank=True, on_delete=models.CASCADE)
#     client = models.ForeignKey(("Client"), null=True, blank=True, on_delete=models.CASCADE)
#     user_activity_time = models.DateTimeField(auto_now_add=True)
#     deleted_flag = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     ingestion_timestamp = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user + " " + self.user_action + " " + self.user_activity_time


# class UserAction(models.Model):
#     user = models.ForeignKey(("User"), null=True, blank=True, on_delete=models.CASCADE)
#     action_name = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     ingestion_timestamp = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user + " " + self.action_name


class BillingLog(models.Model):
    BILLING_STATUS_CHOICES = (
        ('Paid','Paid'),
        ('Unpaid','Unpaid'),
        ('Cancelled', 'Cancelled'),
    )

    company = models.ForeignKey(("Company"), null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(("Plan"), null=True, blank=True, on_delete=models.CASCADE)
    billing_date = models.DateTimeField(auto_now_add=True)
    billing_amount = models.DecimalField(max_digits=100000000000, decimal_places=2)
    billing_status = models.CharField(choices=BILLING_STATUS_CHOICES, max_length=30)
    billing_period_start_date = models.DateTimeField(auto_now_add=True)
    billing_period_end_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company + " " + self.billing_status


class Plan(models.Model):
    PLAN_NAME_CHOICES = (
        ('Basic','Basic'),
        ('Standart','Standart'),
        ('Premium', 'Premium'),
    )

    PLAN_CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    )

    PLAN_TRIAL_PERIOD_CHOICES = (
        ('Yes','Yes'),
        ('No','No'),
    )

    plan_name = models.CharField(choices=PLAN_NAME_CHOICES, max_length=30)
    plan_frequency = models.CharField(max_length=50)
    plan_price = models.DecimalField(max_digits=100000000000, decimal_places=2)
    plan_currency = models.CharField(choices=PLAN_CURRENCY_CHOICES, max_length=10)
    plan_description = models.TextField(max_length=200)
    plan_trial_period = models.CharField(choices=PLAN_TRIAL_PERIOD_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingestion_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name


# class SoftDeleteModel(models.Model):

#     deleted_flag = models.BooleanField(default=False)

#     def soft_delete(self):
#         self.deleted_flag = True
#         self.save()

#     def restore(self):
#         self.deleted_flag = False
#         self.save()

#     class Meta:
#         abstract = True


