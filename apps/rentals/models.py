from django.db import models

# Create your models here.
from decimal import Decimal


class RentalStatus(models.TextChoices):
    # DRAFT = "DRAFT", "Draft"
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    ACTIVE = "ACTIVE", "Active"
    INSPECTION = "INSPECTION", "Inspection"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    OVERDUE = "OVERDUE", "Overdue"
    EXPIRED = "EXPIRED", "Expired"


class RentalItemStatus(models.TextChoices):
    # DRAFT = "DRAFT", "Draft"
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    ACTIVE = "ACTIVE", "Active"
    INSPECTION = "INSPECTION", "Inspection"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    OVERDUE = "OVERDUE", "Overdue"
    EXPIRED = "EXPIRED", "Expired"


class Rental(models.Model):

    # -------------------------------------------------------------------------
    # Relations & Locations
    # -------------------------------------------------------------------------
    customer = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="customer_rentals",
    )
    pickup_location = models.ForeignKey(
        "locations.Location",
        on_delete=models.PROTECT,
        related_name="pickup_rentals",
    )
    return_location = models.ForeignKey(
        "locations.Location",
        on_delete=models.PROTECT,
        related_name="return_rentals",
    )

    # -------------------------------------------------------------------------
    # Order Status & Financial Summary
    # -------------------------------------------------------------------------
    status = models.CharField(
        max_length=40, choices=RentalStatus.choices, default=RentalStatus.PENDING
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    late_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    damage_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    security_deposit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # -------------------------------------------------------------------------
    # Notes & Cancellation Info
    # -------------------------------------------------------------------------
    notes = models.TextField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    # -------------------------------------------------------------------------
    # Workflow Timestamps
    # -------------------------------------------------------------------------
    confirmed_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # System Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Rental"

        constraints = [
        models.CheckConstraint(
            condition=models.Q(subtotal__gte=0),
            name="rental_subtotal_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(discount_amount__gte=0),
            name="rental_discount_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(late_fee__gte=0),
            name="rental_late_fee_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(damage_charge__gte=0),
            name="rental_damage_charge_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(security_deposit__gte=0),
            name="rental_security_deposit_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(total_amount__gte=0),
            name="rental_total_nonnegative",
        ),
    ]

    def __str__(self):
        return f"Rental #{self.id} - {self.customer}"


class RentalItem(models.Model):

    # -------------------------------------------------------------------------
    # Relations
    # -------------------------------------------------------------------------
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name="rental_items",
    )
    equipment = models.ForeignKey(
        "equipments.Equipment",
        on_delete=models.PROTECT,
        related_name="equipment_rental_items",
    )

    # -------------------------------------------------------------------------
    # Dates & Quantities
    # -------------------------------------------------------------------------
    start_at = models.DateField()
    end_at = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    rental_days = models.PositiveIntegerField(default=1)

    # -------------------------------------------------------------------------
    # Pricing Snapshots & Line Totals
    # -------------------------------------------------------------------------
    unit_daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        
    )
    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
       
    )
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # -------------------------------------------------------------------------
    # Tracking & Actual Dates
    # -------------------------------------------------------------------------
    status = models.CharField(
        max_length=40,
        choices=RentalItemStatus.choices,
        default=RentalItemStatus.PENDING,
    )
    confirmed_at = models.DateTimeField(blank=True, null=True)
    actual_pickup_at = models.DateTimeField(null=True, blank=True)
    actual_return_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    # System Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Rental_Item"

        constraints = [
        models.CheckConstraint(
            condition=models.Q(
                end_at__gt=models.F("start_at")
            ),
            name="rental_item_end_after_start",
        ),
        models.CheckConstraint(
            condition=models.Q(unit_daily_rate__gte=0),
            name="rental_item_daily_rate_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(security_deposit__gte=0),
            name="rental_item_deposit_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(late_fee__gte=0),
            name="rental_item_late_fee_nonnegative",
        ),
        models.CheckConstraint(
            condition=models.Q(line_total__gte=0),
            name="rental_item_line_total_nonnegative",
        ),
    ]

    def __str__(self):
        return f"{self.equipment} (Rental #{self.rental_id})"
