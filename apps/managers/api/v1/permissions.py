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

    