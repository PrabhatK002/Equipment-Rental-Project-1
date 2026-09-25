from django.contrib import admin

from apps.equipments.models import Category, Equipment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["is_active"]



@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "location"]
    list_filter = ["condition", "status"]

