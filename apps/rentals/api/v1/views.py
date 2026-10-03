from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import RoleChoice
from apps.carts.models import Cart
from apps.payments.models import Payment, PaymentStatus
from apps.rentals.models import Rental, RentalStatus
from apps.rentals.rental_services import (
    RentalService,
    create_payment_log,
    is_available,
    send_request_khalti,
)
from apps.rentals.api.v1.serializers import (
    CheckoutSerializer,
    RentalSerializer,
    InitiatePaymentSerializer,
    InitiatePaymentResponseSerializer,
    CheckoutResponseSerializer
)
from drf_spectacular.utils import extend_schema
import os

# print(os.getenv("DATABASE"))


@extend_schema(
    request=CheckoutSerializer,
    responses={201: CheckoutResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_checkout(request):

    serializer = CheckoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    cart_id = serializer.validated_data["cart"]
    cart_item_ids = serializer.validated_data["cart_item_ids"]
    pickup_location_id = serializer.validated_data["pickup_location_id"]
    return_location_id = serializer.validated_data["return_location_id"]

    cart = get_object_or_404(Cart, id=cart_id)

    if request.user.role == RoleChoice.CUSTOMER:
        # cart = request.data.get("cart")
        if cart.customer != request.user:
            return Response(
                {"message": "Not the owner of the cart."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # cart_items = cart.cart_items.all()
    # item_ids = []
    # for item in cart_items:
    #     item_ids.append(item.id)

    # # cart_item_ids = request.data.get("cart_item_ids")
    # for cart_item_id in cart_item_ids:
    #     if cart_item_id not in item_ids:
    #         return Response(
    #             {"message": "Cart items don't exist in the provided cart."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    rental_service = RentalService()

    locked_equipments = rental_service.lock_equipments(
        cart=cart, cart_item_ids=cart_item_ids
    )

    # if not_locked_equipments:
    #     return Response(
    #         {
    #             "code": "EQUIPMENT_LOCKED",
    #             "detail": "Some equipment is currently being processed by another transaction.",
    #             "not_locked_equipments": not_locked_equipments,
    #         },
    #         status=status.HTTP_409_CONFLICT,  # 409 Conflict is standard for resource lock contention
    #     )

    availabilities = is_available(cart=cart, cart_item_ids=cart_item_ids)

    if any(not item.get("available") for item in availabilities):
        return Response(
            {"code": "CHECKOUT_VALIDATION_FAILED", "items": availabilities},
            status=status.HTTP_400_BAD_REQUEST,
        )

    sub_total = rental_service.calculate_sub_total(
        cart=cart, cart_item_ids=cart_item_ids
    )
    security_deposit = rental_service.calculate_security_deposit(
        cart=cart, cart_item_ids=cart_item_ids
    )

    rental = rental_service.create_rental(
        cart=cart,
        cart_item_ids=cart_item_ids,
        pickup_location_id=pickup_location_id,
        return_location_id=return_location_id,
        sub_total=sub_total,
        security_deposit=security_deposit,
    )

    rental_service.create_rental_items(
        rental=rental, cart=cart, cart_item_ids=cart_item_ids
    )

    # if request.user.role in [
    #     RoleChoice.ADMIN,
    #     RoleChoice.MANAGER,
    # ]:  # For managers and admins
    #     cart_items = cart.cart_items.all()
    #     item_ids = []
    #     for item in cart_items:
    #         item_ids.append(item.id)

    #     # cart_item_ids = request.data.get("cart_item_ids")
    #     for cart_item_id in cart_item_ids:
    #         if cart_item_id not in item_ids:
    #             return Response(
    #                 {"message": "Cart items don't exist in the provided cart."},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #     rental_service = RentalService()

    #     locked_equipments, not_locked_equipments = rental_service.lock_equipments(
    #         cart=cart, cart_item_ids=cart_item_ids
    #     )

    #     if not_locked_equipments:
    #         return Response(
    #             {
    #                 "code": "EQUIPMENT_LOCKED",
    #                 "detail": "Some equipment is currently being processed by another transaction.",
    #                 "not_locked_equipments": not_locked_equipments,
    #             },
    #             status=status.HTTP_409_CONFLICT,
    #         )

    #     availabilities = is_available(cart=cart, cart_item_ids=cart_item_ids)

    #     if any(not item.get("available") for item in availabilities):
    #         return Response(
    #             {"code": "CHECKOUT_VALIDATION_FAILED", "items": availabilities},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     sub_total = rental_service.calculate_sub_total(
    #         cart=cart, cart_item_ids=cart_item_ids
    #     )

    #     security_deposit = rental_service.calculate_security_deposit(
    #         cart=cart, cart_item_ids=cart_item_ids
    #     )

    #     rental = rental_service.create_rental(
    #         cart=cart,
    #         cart_item_ids=cart_item_ids,
    #         pickup_location_id=pickup_location_id,
    #         return_location_id=return_location_id,
    #         sub_total=sub_total,
    #         security_deposit=security_deposit,
    #     )

    #     rental_service.create_rental_items(
    #         rental=rental, cart=cart, cart_item_ids=cart_item_ids
    #     )

    rental_serializer = RentalSerializer(rental)

    return Response(
        {
            "message": "Rental created successfully.",
            "rental": rental_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    request=InitiatePaymentSerializer,
    responses={
        200: InitiatePaymentResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def initiate_rental_payment(request):

    serializer = InitiatePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rental_id = serializer.validated_data["rental_id"]

    rental = get_object_or_404(Rental, id=rental_id)

    if request.user.role == RoleChoice.CUSTOMER:
        if request.user != rental.customer:
            return Response(
                {"message": "User is not the owner of the rental."},
                status=status.HTTP_403_FORBIDDEN,
            )

    if rental.status != RentalStatus.PENDING:
        return Response(
            {"message": "Only pending rentals can be confirmed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing_payment = Payment.objects.filter(
        rental=rental,
        status__in=[
            PaymentStatus.PENDING,
            PaymentStatus.INITIATED,
        ],
    ).first()

    if existing_payment:
        return Response(
            {"message": "A payment is already pending for this rental."},
            status=status.HTTP_409_CONFLICT,
        )

    khalti_response = send_request_khalti(
        order_id=rental.id,
        order_name="Equipment(s) Rental",
        customer_name=rental.customer.username,
        customer_email=rental.customer.email,
        customer_phone=rental.customer.phone,
        rental_total=rental.total_amount,
        security_deposit=rental.security_deposit,
        rental_name=rental.id,
        total_amount=(rental.total_amount + rental.security_deposit),
    )

    total_amount = rental.total_amount + rental.security_deposit
    notes = f"Rental #{rental.id} with security deposit {rental.security_deposit}, rental total {rental.total_amount} and total amount {rental.security_deposit + rental.total_amount}"

    pidx = khalti_response.get("pidx")
    payment_url = khalti_response.get("payment_url")

    if not pidx or not payment_url:
        return Response(
            {
                "message": "Unable to initiate Khalti payment.",
                "provider_response": khalti_response,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    create_payment_log(
        rental=rental,
        customer=rental.customer,
        amount=total_amount,
        provider="khalti",
        provider_payment_id=khalti_response["pidx"],
        currency="NPR",
        notes=notes,
    )

    return Response(
        {
            "message": "Rental payment request successful.",
            "khalti_response": khalti_response,
        },
        status=status.HTTP_200_OK,
    )
