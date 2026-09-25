from django.contrib import admin

from apps.locations.models import Location

# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display =["name", "code", "address"]
    list_filter = ["city"]