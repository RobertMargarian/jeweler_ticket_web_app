# Generated by Django 4.2.3 on 2023-07-27 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_remove_order_work_order_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_role',
            name='user_role_name',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Manager', 'Manager'), ('Employee', 'Employee')], max_length=30),
        ),
    ]
