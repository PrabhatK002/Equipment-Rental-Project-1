from rest_framework.permissions import BasePermission

from apps.accounts.models import RoleChoice


class AdminManagerPermission(BasePermission):

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method == "GET":
            return True

        return request.user.role in [RoleChoice.MANAGER, RoleChoice.ADMIN]