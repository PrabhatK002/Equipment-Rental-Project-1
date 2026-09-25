from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

# Create your models here.


class Condition(models.TextChoices):
    NEW = "new", "New"
    GOOD = "good", "Good"
    FAIR = "fair", "Fair"
    DAMAGED = "damaged", "Damaged"


class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    MAINTENANCE = "maintenance", "Maintenance"
    RETIRED = "retired", "Retired"
    UNAVAILABLE = "unavailable", "Unavailable"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Equipment(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="equipment",
    )

    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.PROTECT,
        related_name="equipment",
    )

    name = models.CharField(
        max_length=255,
    )

    asset_code = models.CharField(
        max_length=100,
        unique=True,
    )

    serial_number = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    weekly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    replacement_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "equipments"

        constraints = [
            models.CheckConstraint(
                condition=Q(daily_rate__gt=0),
                name="equipment_daily_rate_gt_zero",
            ),
            models.CheckConstraint(
                condition=Q(weekly_rate__gt=0),
                name="equipment_weekly_rate_gt_zero",
            ),
            models.CheckConstraint(
                condition=Q(security_deposit__gt=0),
                name="equipment_security_deposit_gt_zero",
            ),
            models.CheckConstraint(
                condition=Q(replacement_value__gt=0),
                name="equipment_replacement_value_gt_zero",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.asset_code})"
