from django.db import models

# Create your models here.
from decimal import Decimal

class RentalStatus(models.TextChoices):
        #DRAFT = "DRAFT", "Draft"
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        OVERDUE = "OVERDUE", "Overdue"
        EXPIRED = "EXPIRED", "Expired"

class RentalItemStatus(models.TextChoices):
        #DRAFT = "DRAFT", "Draft"
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        OVERDUE = "OVERDUE", "Overdue"
        EXPIRED = "EXPIRED", "Expired"

class Rental(models.Model):

    # -------------------------------------------------------------------------
    # Relations & Locations
    # -------------------------------------------------------------------------
    customer = models.ForeignKey(
        'customers.CustomerProfile',
        on_delete=models.PROTECT,
        related_name="customer_rentals"
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
        max_length=40,
        choices=RentalStatus.choices,
        default=RentalStatus.PENDING
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
    quantity = models.PositiveIntegerField(
        default=1)
    rental_days = models.PositiveIntegerField(
        default=1)

    # -------------------------------------------------------------------------
    # Pricing Snapshots & Line Totals
    # -------------------------------------------------------------------------
    unit_daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),)
    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),)
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),)
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),)

    # -------------------------------------------------------------------------
    # Tracking & Actual Dates
    # -------------------------------------------------------------------------
    status = models.CharField(
        max_length=40,
        choices=RentalItemStatus.choices,
        default=RentalItemStatus.PENDING
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

    def __str__(self):
        return f"{self.equipment} (Rental #{self.rental_id})"

    # def calculate_rental_days(self):
    #     """Calculates billable days (minimum 1 day). Partial days round up."""
    #     if self.start_at and self.end_at and self.end_at > self.start_at:
    #         delta = self.end_at - self.start_at
    #         days = math.ceil(delta.total_seconds() / 86400)
    #         return max(1, days)
    #     return 1

    # def calculate_line_total(self):
    #     """
    #     Calculates total for this item.
    #     Uses weekly rate if 7+ days and weekly_rate_snapshot is defined;
    #     otherwise uses daily rate.
    #     """
    #     self.rental_days = self.calculate_rental_days()

    #     if not self.unit_daily_rate:
    #         self.line_total = Decimal("0.00")
    #         return self.line_total

    #     # Example weekly vs daily rate logic
    #     if self.weekly_rate_snapshot and self.rental_days >= 7:
    #         weeks = self.rental_days // 7
    #         remaining_days = self.rental_days % 7
    #         base_total = (weeks * self.weekly_rate_snapshot) + (remaining_days * self.unit_daily_rate)
    #     else:
    #         base_total = Decimal(self.rental_days) * self.unit_daily_rate

    #     self.line_total = base_total * Decimal(self.quantity)
    #     return self.line_total

    # def save(self, *args, **kwargs):
    #     # Auto-populate unit rates from Equipment if not explicitly provided
    #     if not self.unit_daily_rate and self.equipment_id:
    #         self.unit_daily_rate = getattr(self.equipment, "daily_rate", Decimal("0.00"))
    #         if not self.weekly_rate_snapshot:
    #             self.weekly_rate_snapshot = getattr(self.equipment, "weekly_rate", None)

    #     # Recalculate duration and line total
    #     self.calculate_line_total()

    #     super().save(*args, **kwargs)
