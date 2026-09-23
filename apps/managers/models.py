from django.db import models

# Create your models here.


class Manager(models.Model):

    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="manager_profile"
    )
    employee_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "manager_profiles"

    def __str__(self):
        return self.user.username
