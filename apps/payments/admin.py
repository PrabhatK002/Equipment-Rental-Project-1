from django.contrib import admin

from apps.payments.models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdming(admin.ModelAdmin):
    list_display = ['rental', 'customer', 'status']
