from django.contrib import admin

from apps.customers.models import CustomerProfile

# Register your models here.

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "country"]
    list_filter = ["country"]
