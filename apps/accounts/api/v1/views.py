from apps.accounts.api.v1.serializers import RegisterSerializer, UserInfoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from apps.accounts.models import RoleChoice
from apps.customers.api.v1.serializers import CustomerProfileSerializer
from apps.customers.models import CustomerProfile
from apps.managers.models import Manager
from apps.managers.api.v1.serializers import ManagerSerializer


@api_view(["POST"])
def register(request):
    request_data = request.data
    serializer = RegisterSerializer(data=request_data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request_data["password"])
        user.save()
        return Response({"message": "Register Successfully"}, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def me(request):
    user_serializer = UserInfoSerializer(request.user)

    profile_serializer = None

    if request.user.role == RoleChoice.CUSTOMER:
        profile = CustomerProfile.objects.filter(user=request.user).first()

        if profile:
            profile_serializer = CustomerProfileSerializer(profile)

    elif request.user.role == RoleChoice.MANAGER:
        profile = Manager.objects.filter(user=request.user).first()

        if profile:
            profile_serializer = ManagerSerializer(profile)

    return Response(
        {
            "user": user_serializer.data,
            "profile": profile_serializer.data if profile_serializer else None,
        },
        status=status.HTTP_200_OK,
    )
