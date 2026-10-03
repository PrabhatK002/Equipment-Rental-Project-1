from apps.carts.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q

from apps.equipments.models import Equipment, Status
from apps.locations.models import Location
from apps.maintenances.models import Maintenance, MaintenanceStatus
from apps.rentals.models import RentalItemStatus, RentalStatus, Rental, RentalItem
from datetime import timedelta

import requests
import json
import os
import uuid
from apps.payments.models import Payment, PaymentStatus


def create_cart(user):
    customer = user

    cart = Cart.objects.create(customer=customer)

    return cart


class RentalService:

    def create_rental(
        self,
        cart,
        cart_item_ids,
        pickup_location_id,
        return_location_id,
        sub_total,
        security_deposit,
    ):
        customer = cart.customer
        pickup_location = get_object_or_404(Location, id=pickup_location_id)
        return_location = get_object_or_404(Location, id=return_location_id)
        status = RentalStatus.PENDING
        sub_total = sub_total
        discount = 0
        security_deposit = security_deposit
        total_amount = sub_total - discount

        rental = Rental.objects.create(
            customer=customer,
            pickup_location=pickup_location,
            return_location=return_location,
            status=status,
            subtotal=sub_total,
            discount_amount=discount,
            security_deposit=security_deposit,
            total_amount=total_amount,
        )

        return rental

    def calculate_sub_total(self, cart, cart_item_ids):
        sub_total = 0
        for cart_item_id in cart_item_ids:
            cart_item = CartItem.objects.filter(id=cart_item_id).first()
            equipment = cart_item.equipment
            start_at = cart_item.start_date
            end_at = cart_item.end_date
            quantity = 1

            unit_daily_rate = equipment.daily_rate

            days = (end_at - start_at).days
            rental_days = max(1, days)

            line_total = rental_days * unit_daily_rate

            sub_total += line_total

        return sub_total

    def calculate_security_deposit(self, cart, cart_item_ids):
        final_security_deposit = 0
        for cart_item_id in cart_item_ids:
            cart_item = CartItem.objects.filter(id=cart_item_id).first()

            equipment = cart_item.equipment
            security_deposit = equipment.security_deposit

            final_security_deposit += security_deposit

        return final_security_deposit

    def create_rental_items(self, rental, cart, cart_item_ids):
        for cart_item_id in cart_item_ids:
            rental = rental
            cart_item = CartItem.objects.filter(id=cart_item_id).first()

            equipment = cart_item.equipment
            start_at = cart_item.start_date
            end_at = cart_item.end_date
            quantity = 1

            unit_daily_rate = equipment.daily_rate
            security_deposit = equipment.security_deposit

            days = (end_at - start_at).days
            rental_days = max(1, days)

            line_total = rental_days * unit_daily_rate
            status = RentalItemStatus.PENDING

            RentalItem.objects.create(
                rental=rental,
                equipment=equipment,
                start_at=start_at,
                end_at=end_at,
                quantity=quantity,
                rental_days=rental_days,
                unit_daily_rate=unit_daily_rate,
                security_deposit=security_deposit,
                line_total=line_total,
                status=status,
            )

    @transaction.atomic
    def lock_equipments(self, cart, cart_item_ids):
        equipment_ids = list(
            cart.cart_items.filter(id__in=cart_item_ids)
            .values_list("equipment_id", flat=True)
            .distinct()
        )

        locked_equipments = list(
            Equipment.objects.select_for_update()
            .filter(id__in=equipment_ids)
            .order_by("id")
        )

        return locked_equipments

    # @transaction.atomic
    # def lock_equipments(self, cart, cart_item_ids):
    #     equipment_ids = (
    #         cart.cart_items.filter(id__in=cart_item_ids)
    #         .values_list("equipment_id", flat=True)
    #         .distinct()
    #     )

    #     if not equipment_ids:
    #         return [], []

    #     locked_equipments = []
    #     not_locked_equipments = []

    #     for eq_id in equipment_ids:
    #         try:
    #             equipment = Equipment.objects.select_for_update(nowait=True).get(
    #                 id=eq_id
    #             )
    #             locked_equipments.append(equipment)
    #         except Exception:
    #             failed_item = Equipment.objects.filter(id=eq_id).first()
    #             if failed_item:
    #                 not_locked_equipments.append(failed_item.name)

    #     return locked_equipments, not_locked_equipments


def is_available(cart, cart_item_ids):
    availabilities = []
    inspection_buffer = timedelta(days=1)
    for cart_item_id in cart_item_ids:
        cart_item = CartItem.objects.filter(id=cart_item_id).first()

        equipment = cart_item.equipment
        requested_start_at = cart_item.start_date
        requested_end_at = cart_item.end_date

        if equipment.status in [
            Status.RETIRED,
            Status.UNAVAILABLE,
        ]:
            availability = {
                "cart_item_id": cart_item_id,
                "equipment_id": equipment.id,
                "equipment_name": equipment.name,
                "available": False,
                "reason": equipment.status,
                "requested_start": requested_start_at,
                "requested_end": requested_end_at,
            }

            availabilities.append(availability)

        # elif equipment.status == Status.MAINTENANCE:
        #     maintenance_conflict = Maintenance.objects.filter(
        #         equipment=equipment,
        #         start_at__lte=requested_end_at,
        #         end_at__gte=requested_start_at,
        #         status__in=[
        #             MaintenanceStatus.SCHEDULED,
        #             MaintenanceStatus.IN_PROGRESS,
        #         ],
        #     ).first()
        #     if maintenance_conflict:
        #         maintenance_start_at = maintenance_conflict.start_at
        #         maintenance_end_at = maintenance_conflict.end_at

        #         availability = {
        #             "cart_item_id": cart_item_id,
        #             "equipment_id": equipment.id,
        #             "equipment_name": equipment.name,
        #             "available": False,
        #             "reason": "Equipment Maintenance",
        #             "requested_start": requested_start_at,
        #             "requested_end": requested_end_at,
        #             "maintenance_start_at": maintenance_start_at,
        #             "maintenance_end_at": maintenance_end_at,
        #         }

        #         availabilities.append(availability)

        #     elif not maintenance_conflict:
        #         availability = {
        #             "cart_item_id": cart_item_id,
        #             "equipment_id": equipment.id,
        #             "equipment_name": equipment.name,
        #             "available": True,
        #             "reason": "Equipment Maintenance not conflict",
        #             "requested_start": requested_start_at,
        #             "requested_end": requested_end_at,

        #         }

        #         availabilities.append(availability)

        elif equipment.status in [Status.ACTIVE, Status.MAINTENANCE]:
            maintenance_conflict = Maintenance.objects.filter(
                equipment=equipment,
                start_at__lte=(requested_end_at + inspection_buffer),
                end_at__gte=(requested_start_at - inspection_buffer),
                status__in=[
                    MaintenanceStatus.SCHEDULED,
                    MaintenanceStatus.IN_PROGRESS,
                ],
            ).first()

            rental_conflict = (
                RentalItem.objects.filter(
                    equipment=equipment,
                    start_at__lte=(requested_end_at + inspection_buffer),
                    end_at__gte=(requested_start_at - inspection_buffer),
                )
                .exclude(
                    status__in=[
                        # RentalItemStatus.PENDING,
                        RentalItemStatus.CANCELLED,
                        RentalItemStatus.EXPIRED,
                        RentalItemStatus.COMPLETED,
                    ]
                )
                .first()
            )

            if maintenance_conflict:
                maintenance_start_at = maintenance_conflict.start_at
                maintenance_end_at = maintenance_conflict.end_at

                availability = {
                    "cart_item_id": cart_item_id,
                    "equipment_id": equipment.id,
                    "equipment_name": equipment.name,
                    "available": False,
                    "reason": "Equipment Maintenance",
                    "requested_start": requested_start_at,
                    "requested_end": requested_end_at,
                    "maintenance_start_at": maintenance_start_at,
                    "maintenance_end_at": maintenance_end_at,
                }

                availabilities.append(availability)

            elif rental_conflict:
                rental_start_at = rental_conflict.start_at
                rental_end_at = rental_conflict.end_at

                availability = {
                    "cart_item_id": cart_item_id,
                    "equipment_id": equipment.id,
                    "equipment_name": equipment.name,
                    "available": False,
                    "reason": "Rental Conflict",
                    "requested_start": requested_start_at,
                    "requested_end": requested_end_at,
                    "rental_start_at": rental_start_at,
                    "rental_end_at": rental_end_at,
                }

                availabilities.append(availability)

            else:

                availability = {
                    "cart_item_id": cart_item_id,
                    "equipment_id": equipment.id,
                    "equipment_name": equipment.name,
                    "available": True,
                    "requested_start": requested_start_at,
                    "requested_end": requested_end_at,
                }

                availabilities.append(availability)

    return availabilities


def send_request_khalti(**kwargs):

    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    order_id = kwargs.get("order_id")
    order_name = kwargs.get("order_name")
    customer_name = kwargs.get("customer_name")
    customer_email = kwargs.get("customer_email")
    customer_phone = kwargs.get("customer_phone")
    rental_total = kwargs.get("rental_total")
    security_deposit = kwargs.get("security_deposit")
    rental_name = kwargs.get("rental_name")
    total_amount = kwargs.get("total_amount")

    payload = json.dumps(
        {
            "return_url": "http://127.0.0.1:8000/khalti_callback/", #"http://localhost:8000/khalti_callback/", "http://http://127.0.0.1:8000/khalti_callback/"
            "website_url": "https://broadway.com/",
            "amount": int(total_amount * 100),
            "purchase_order_id": order_id,
            "purchase_order_name": order_name,
            "customer_info": {
                "name": customer_name,
                "email": customer_email,
                "phone": customer_phone,
            },
            "amount_breakdown": [
                {"label": "Sub Total", "amount": int(rental_total * 100)},
                {"label": "Security Deposit", "amount": int(security_deposit * 100)},
            ],
            "product_details": [
                {
                    "identity": "1234567890",
                    "name": rental_name,
                    "total_price": int(total_amount * 100),
                    "quantity": 1,
                    "unit_price": int(total_amount * 100),
                }
            ],
        }
    )
    headers = {
        "Authorization": f"Key {os.getenv('LIVE_KEY_KHALTI')}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def create_payment_log(**kwargs):
    payment = Payment.objects.create(
        rental=kwargs.get("rental"),
        customer=kwargs.get("customer"),
        transaction_id=str(uuid.uuid4()),
        amount=kwargs.get("amount"),
        provider=kwargs.get("provider", "khalti"),
        provider_payment_id=kwargs.get("provider_payment_id"),
        currency=kwargs.get("currency"),
        notes=kwargs.get("notes"),
    )
    return payment


def verify_khalti_payment(pidx):
    url = "https://dev.khalti.com/api/v2/epayment/lookup/"

    headers = {
        "Authorization": f"Key {os.getenv('LIVE_KEY_KHALTI')}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={"pidx": pidx},
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

# key = os.getenv("LIVE_KEY_KHALTI")
# print("Key loaded:", bool(key))