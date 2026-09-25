from django.db import models

# Create your models here.


class Cart(models.Model):
    customer = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="customer_cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    equipment = models.ForeignKey(
        "equipments.Equipment",
        on_delete=models.PROTECT,
        related_name="cart_items",
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.equipment.asset_code}"
