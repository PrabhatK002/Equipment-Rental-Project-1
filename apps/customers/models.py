from django.db import models

# Create your models here.

class CustomerProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name="customer_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(max_length=500, blank=True)
    country = models.TextField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Customer_Profile"

    def __str__(self):
        return self.user.username