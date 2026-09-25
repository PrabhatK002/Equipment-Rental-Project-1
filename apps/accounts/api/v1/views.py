from django.db import transaction

from apps.accounts.api.v1.serializers import RegisterSerializer, UserInfoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status

from django.shortcuts import get_object_or_404

from apps.accounts.models import RoleChoice
from apps.customers.api.v1.serializers import CustomerProfileSerializer
from apps.customers.models import CustomerProfile
from apps.managers.models import Manager
from apps.managers.api.v1.serializers import ManagerSerializer

from drf_spectacular.utils import extend_schema

from apps.rentals.api.v1.services import create_cart


@extend_schema(
    request=RegisterSerializer,
    responses={201: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def customer_register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save(role=RoleChoice.CUSTOMER)

        user.set_password(request.data["password"])
        user.save()
        create_cart(user=user)

        return Response(
            {"message": "Registered successfully"},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    request=RegisterSerializer,
    responses={201: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def manager_register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save(role=RoleChoice.MANAGER)

        user.set_password(request.data["password"])
        user.save()

        return Response(
            {"message": "Registered successfully"},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    responses={
        200: UserInfoSerializer
    }  # Tells Swagger what schema to expect on success
)
@api_view(["GET"])
def me(request):
    serializer_class = UserInfoSerializer
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
