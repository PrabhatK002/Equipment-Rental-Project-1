from django.contrib import admin

from apps.rentals.models import Rental, RentalItem

# Register your models here.
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['customer', 'security_deposit', 'total_amount']


@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ['rental', 'equipment', 'security_deposit', 'line_total']