from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema 

from apps.customers.models import CustomerProfile
from apps.customers.api.v1.serializers import CustomerProfileSerializer
from .permission import CustomerPermission


class CustomerProfileView(GenericAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [CustomerPermission]

    @extend_schema(operation_id="list_customer_profiles")
    def get(self, request):
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)

            return Response(
                {"message": "Customer profile posted successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileDetailView(GenericAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [CustomerPermission]

    @extend_schema(operation_id="retrieve_customer")
    def get(self, request, pk):
        customer = self.get_object()
        serializer = self.get_serializer(customer)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        customer = self.get_object()
        serializer = self.get_serializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Customer profile updated successfully."},
                status.HTTP_200_OK,
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        customer = self.get_object()
        serializer = self.get_serializer(customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Customer profile updated successfully."},
                status.HTTP_200_OK,
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object()

        customer.delete()

        return Response({"message": "Customer profile deleted successfully."})
