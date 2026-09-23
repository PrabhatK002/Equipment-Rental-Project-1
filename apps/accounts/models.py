from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class RoleChoice(models.TextChoices):
    ADMIN = "Admin"
    MANAGER = "Manager"
    CUSTOMER = "Customer"

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.CUSTOMER)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # def __str__(self):
    #     return f"{self.get_full_name() or self.username} ({self.role})"