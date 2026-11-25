from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from apps.maintenances.models import Maintenance
from apps.maintenances.api.v1.serializers import MaintenanceSerializer
from apps.maintenances.api.v1.permissions import MaintenancePermission


class MaintenanceView(GenericAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.all()
    permission_classes = [MaintenancePermission]


    def get(self, request):
        maintenances = self.get_queryset()
        serializer = self.get_serializer(maintenances, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                {
                    "message": "Maintenance of equipment posted successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)




class MaintenanceDetailView(GenericAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.all()
    permission_classes = [MaintenancePermission]

    def get(self, request):
        maintenance = self.get_object()
        serializer = self.get_serializer(maintenance)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request):
        maintenance = self.get_object()
        serializer = self.get_serializer(maintenance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Maintenance updated successfully."
                },
                status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        maintenance = self.get_object()
        serializer = self.get_serializer(maintenance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Maintenance updated successfully."
                },
                status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        maintenance = self.get_object()
        maintenance.delete()

        return Response(
            {
                "message":"Maintenance deleted successfully."
            },
            status.HTTP_200_OK
        )

    
