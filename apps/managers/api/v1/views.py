from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema

from apps.accounts.models import RoleChoice
from apps.managers.api.v1.permissions import ManagerProfilePermission
from apps.managers.api.v1.serializers import ManagerSerializer
from apps.managers.models import Manager


class ManagerView(APIView):
    serializer_class = ManagerSerializer
    permission_classes = [ManagerProfilePermission]

    @extend_schema(operation_id="list_manager_profiles")
    def get(self, request):
        if request.user.role == RoleChoice.ADMIN:
            managers = Manager.objects.all()
        else:
            managers = Manager.objects.filter(user=request.user)

        serializer = ManagerSerializer(managers, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Manager profile posted successfully."},
                status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ManagerDetailView(APIView):
    serializer_class = ManagerSerializer
    permission_classes = [ManagerProfilePermission]

    @extend_schema(operation_id="retrieve_manager_profile")
    def get(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        serializer = ManagerSerializer(manager)

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        serializer = ManagerSerializer(manager, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Manager profile updated successfully."}, status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        serializer = ManagerSerializer(manager, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Manager profile updated successfully."}, status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)

        manager.delete()

        return Response(
            {"message": "Manager profile deleted successfully."}, status.HTTP_200_OK
        )
