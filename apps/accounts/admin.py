from django.contrib import admin
from apps.accounts.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.
@admin.register(User)
class UserAdminInterface(UserAdmin):
   useradmin_fieldset = UserAdmin.fieldsets
   extra = (
        ('Extra Info', {'fields': ('role', 'phone')}),
    )
   fieldsets = useradmin_fieldset + extra


