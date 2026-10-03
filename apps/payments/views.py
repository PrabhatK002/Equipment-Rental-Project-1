from django.shortcuts import render

from datetime import datetime
from django.http import HttpResponse

from apps.payments.models import Payment, PaymentStatus
from apps.rentals.models import Rental, RentalStatus, RentalItem
from apps.rentals.rental_services import verify_khalti_payment
from django.utils import timezone
from apps.rentals.models import RentalItemStatus

# Create your views here.


def khalti_callback(request):
    data = request.GET
    pidx = request.GET.get("pidx")

    payment = (
        Payment.objects.filter(provider_payment_id=pidx)
        .select_related("rental")
        .first()
    )
    if not payment:
        return HttpResponse("pidx doesnot exist")
    rental = payment.rental
    #payment = payment.first()
    lookup = verify_khalti_payment(pidx)

    expected_amount = int(payment.amount * 100)

    if lookup.get("total_amount") != expected_amount:
        return HttpResponse(
            "Payment amount mismatch.",
            status=400,
        )

    if lookup.get("status") == "Completed":
        rental.status = RentalStatus.CONFIRMED
        rental.confirmed_at = timezone.now()
        rental.save(
            update_fields=[
                "status",
                "confirmed_at",
            ]
        )

        rental.rental_items.filter(status=RentalItemStatus.PENDING).update(
            status=RentalItemStatus.CONFIRMED,
            confirmed_at=timezone.now(),
        )

        payment.status = PaymentStatus.SUCCEEDED
        payment.provider_transaction_id = data["tidx"]
        payment.paid_at=timezone.now()
        payment.save()

    else:
        payment.status = PaymentStatus.CANCELLED
        payment.save()
    context = {"payment": payment}
    return render(request, "payments/index.html", context)
