from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    items: models.Manager

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        """Calculate the total price of items in the cart"""
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"