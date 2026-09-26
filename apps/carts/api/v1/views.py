from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404

from apps.carts.models import CartItem, Cart
from apps.carts.api.v1.serializers import CartSerializer, CartItemSerializer
from apps.carts.api.v1.permissions import CartPermission, CartItemsPermission


class CartView(GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CartPermission]

    def get(self, request):
        cart = Cart.objects.filter(customer=request.user)
        serializer = self.get_serializer(cart)

        return Response(serializer.data, status.HTTP_200_OK)



class CartItemView(GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CartItemsPermission]


    def get(self, request):
        cart_items = CartItem.objects.filter(cart=request.data.get("cart"))
        serializer = self.get_serializer(cart_items, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Cart Item saved successfully to the cart."
                },
                status.HTTP_201_CREATED
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
                {
                    "message":"Cart Item updated successfully."
                },
                status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
            cart_item = self.get_object()
            serializer = self.get_serializer(cart_item, data=request.data, partial=True)
    
            if serializer.is_valid():
                serializer.save()
    
                return Response(
                    {
                        "message":"Cart Item updated successfully."
                    },
                    status.HTTP_200_OK
                )
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object()

        cart_item.delete()

        return Response(
            {
                "message":"Cart Item deleted successfully."
            },
            status.HTTP_200_OK
        )
    


