from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.equipments.models import Category, Equipment
from apps.equipments.api.v1.serializers import CategorySerializer, EquipmentSerializer
from apps.equipments.api.v1.permissions import AdminManagerPermission


class CategoryView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminManagerPermission]

    @extend_schema(operation_id="list_categories")
    def get(self, request):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Category posted successfully."
                },
                status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminManagerPermission]

    @extend_schema(operation_id="retrieve_category")
    def get(self, request, pk):
        category = self.get_object()
        serializer = self.get_serializer(category)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Category updated successfully."
                },
                status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Category updated successfully."
                },
                status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        category = self.get_object()

        category.delete()

        return Response(
            {
                "message":"Category deleted successfully."
            },
            status.HTTP_200_OK
        )


class EquipmentView(GenericAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminManagerPermission]

    @extend_schema(operation_id="list_equipments")
    def get(self, request):
        equipments = self.get_queryset()
        serializer = self.get_serializer(equipments, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Equipment created successfully."
                },
                status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class EquipmentDetailView(GenericAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminManagerPermission]

    @extend_schema(operation_id="retrieve_equipment")
    def get(self, request, pk):
        equipment = self.get_object()
        serializer = self.get_serializer(equipment)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        equipment = self.get_object()
        serializer = self.get_serializer(equipment, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Equipment updated successfully."
                },
                status.HTTP_200_OK)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        equipment = self.get_object()
        serializer = self.get_serializer(equipment, data=request.data)
    
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Equipment updated successfully."
                },
                status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        equipment = self.get_object()

        equipment.delete()

        return Response(
            {
                "message":"Equipment deleted successfully."
            },
            status.HTTP_200_OK
        )

    