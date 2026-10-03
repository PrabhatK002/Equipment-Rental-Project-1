from django.db import models
import uuid

from django.db.models import Q

# Create your models here.


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    INITIATED = "INITIATED", "Initiated"
    SUCCEEDED = "SUCCEEDED", "Succeeded"
    CANCELLED = "CANCELLED", "Cancelled"
    FAILED = "FAILED", "Failed"


class Payment(models.Model):
    rental = models.ForeignKey(
        "rentals.Rental", on_delete=models.PROTECT, related_name="rental_payments"
    )
    customer = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="customer_payments"
    )
    provider = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        choices=PaymentStatus.choices, max_length=30, default=PaymentStatus.PENDING
    )

    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider_transaction_id = models.CharField(max_length=255, blank=True, null=True) #tidx
    provider_payment_id = models.CharField(max_length=50, null=True, blank=True, ) #pidx
    currency = models.CharField(
        max_length=3,
        default="NPR",
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    notes = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Payment"

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="payment_amount_gt_zero",
            ),
        ]

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} "





# class PaymentAllocationType(models.TextChoices):
#     RENTAL = "RENTAL", "Rental Charge"
#     SECURITY_DEPOSIT = "SECURITY_DEPOSIT", "Security Deposit"
#     DAMAGE = "DAMAGE", "Damage Charge"
#     LATE_FEE = "LATE_FEE", "Late Fee"


# class PaymentAllocation(models.Model):
#     payment = models.ForeignKey(
#         Payment,
#         on_delete=models.CASCADE,
#         related_name="allocations",
#     )

#     allocation_type = models.CharField(
#         max_length=30,
#         choices=PaymentAllocationType.choices,
#     )

#     amount = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True,
#     )

#     class Meta:
#         db_table = "payment_allocations"

#         constraints = [
#             models.CheckConstraint(
#                 condition=Q(amount__gt=0),
#                 name="payment_allocation_amount_gt_zero",
#             ),
#         ]