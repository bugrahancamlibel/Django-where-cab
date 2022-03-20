from django.contrib import admin

# Register your models here.
from .models import Customer, Cars

admin.site.register(Customer)
admin.site.register(Cars)
