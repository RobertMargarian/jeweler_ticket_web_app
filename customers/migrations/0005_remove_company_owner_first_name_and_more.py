# Generated by Django 4.2.3 on 2023-07-27 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_user_role_user_role_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='owner_first_name',
        ),
        migrations.RemoveField(
            model_name='company',
            name='owner_last_name',
        ),
        migrations.AlterField(
            model_name='company',
            name='company_subscription_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Canceled', 'Canceled')], max_length=30),
        ),
    ]
