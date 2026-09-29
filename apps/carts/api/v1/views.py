from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404

from apps.accounts.models import RoleChoice
from apps.carts.models import CartItem, Cart
from apps.carts.api.v1.serializers import CartSerializer, CartItemSerializer
from apps.carts.api.v1.permissions import CartPermission, CartItemsPermission


class CartView(GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CartPermission]

    def get(self, request):
        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        ]:
            carts = Cart.objects.all()
            serializer = self.get_serializer(carts, many=True)

        elif request.user.role == RoleChoice.CUSTOMER:
            cart = Cart.objects.get(customer=request.user)
            serializer = self.get_serializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)


class CartDetailView(GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CartPermission]

    def get(self, request, pk):
        cart = self.get_object()
        serializer = self.get_serializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)


class CartItemAdminManagerView(GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CartItemsPermission]

    def get(self, request, pk):
        if request.user.role == RoleChoice.CUSTOMER:
            return Response(
                {"message": "You don't have permission to access this part."},
                status.HTTP_400_BAD_REQUEST,
            )

        cart = get_object_or_404(Cart, pk=pk)

        cart_items = cart.cart_items.all()
        serializer = self.get_serializer(cart_items, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class CartItemView(GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CartItemsPermission]

    def get(self, request):

        if request.user.role in [
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        ]:
            carts_items = CartItem.objects.all()
            serializer = self.get_serializer(carts_items, many=True)
        
        elif request.user.role == RoleChoice.CUSTOMER:
            cart = Cart.objects.get(customer=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            serializer = self.get_serializer(cart_items, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):

        cart_id = request.data.get("cart")
        equipment_id = request.data.get("equipment")

        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            return Response(
                {
                    "message":"Cart is required."
                },
                status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.cart_items.all()
        cart_items_equipments = []

        for cart_item in cart_items:
            cart_items_equipments.append(cart_item.equipment.id)

        if equipment_id in cart_items_equipments:
            return Response(
                {
                    "message":"The equipment already exists in the Cart."
                },
                status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Cart Item saved successfully to the cart."},
                status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CartItemDetailView(GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CartItemsPermission]

    def get(self, request, pk):

        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Cart Item updated successfully."}, status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Cart Item updated successfully."}, status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object()

        cart_item.delete()

        return Response(
            {"message": "Cart Item deleted successfully."}, status.HTTP_200_OK
        )
