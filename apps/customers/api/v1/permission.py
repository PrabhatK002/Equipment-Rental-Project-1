from rest_framework.permissions import BasePermission
from apps.accounts.models import RoleChoice


class CustomerPermission(BasePermission):

    def has_permission(self, request, view):

        # User must be logged in
        if not request.user.is_authenticated:
            return False

        # Admin can access customer profiles
        if request.user.role == RoleChoice.ADMIN:
            return True

        # Customer can access the CustomerProfile API
        if request.user.role == RoleChoice.CUSTOMER:
            return True

        return False

    def has_object_permission(self, request, view, obj):

        # Admin can access any customer profile
        if request.user.role == RoleChoice.ADMIN:
            return True

        # Customer can only access their own profile
        return obj.user == request.user
