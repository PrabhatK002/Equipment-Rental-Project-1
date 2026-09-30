from django.db import models

# Create your models here.
class MaintenanceStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Maintenance(models.Model):
    equipment = models.ForeignKey(
        "equipments.Equipment",
        on_delete=models.PROTECT,
        related_name="maintenances",
    )

    start_at = models.DateField()
    end_at = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.SCHEDULED,
    )

    reason = models.TextField()
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Maintenance"
    