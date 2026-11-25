from rest_framework.permissions import BasePermission

from apps.accounts.models import RoleChoice

class MaintenancePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            return request.user.role in [
                RoleChoice.ADMIN,
                RoleChoice.MANAGER
            ]

        return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method == "GET":
            return True

        return request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER
        ]