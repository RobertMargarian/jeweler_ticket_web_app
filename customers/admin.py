from django.contrib import admin

from .models import Company, User, Order, Client, User_Role, Plan


admin.site.register(Company)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(User_Role)
admin.site.register(Plan)
