from rest_framework.permissions import BasePermission

from apps.accounts.models import RoleChoice


class ManagerProfilePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False


        return request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER
        ]

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == RoleChoice.MANAGER:
            return request.user == obj.user

        if request.user.role == RoleChoice.ADMIN:
            return True

        return False

        

    