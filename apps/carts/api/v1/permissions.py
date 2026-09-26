from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404

from apps.accounts.models import RoleChoice
from apps.carts.models import Cart

class CartPermission(BasePermission):

    def has_permission(self, request, view):
    
        if not request.user.is_authenticated:
            return False

        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        ]:
            return True

        # Customer
        if request.user.role == RoleChoice.CUSTOMER:
            # if request.method == "GET":
            #     customer = request.data.get("customer")

            #     if not customer:
            #         return False

            #     return request.user == customer

            return True

        return False

class CartItemsPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        # Admin and Manager can access everything
        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        ]:
            return True

        # Customer
        if request.user.role == RoleChoice.CUSTOMER:

            # For POST, check the submitted cart
            if request.method == "POST":

                cart_id = request.data.get("cart")

                if not cart_id:
                    return False

                cart = Cart.objects.filter(id=cart_id).first()

                if not cart:
                    return False

                return cart.customer == request.user

            return True

        return False

    def has_object_permission(self, request, view, obj):

        # Admin and Manager can access everything
        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        ]:
            return True

        # Customer can access only their own CartItems
        if request.user.role == RoleChoice.CUSTOMER:
            return obj.cart.customer == request.user

        return False