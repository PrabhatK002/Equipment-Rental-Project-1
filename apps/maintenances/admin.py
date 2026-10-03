from django.contrib import admin

from apps.maintenances.models import Maintenance

# Register your models here.

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'start_at', 'end_at']