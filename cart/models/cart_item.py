from django.db import models

from store.models import Product
from . import Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Calculate the cost of this cart item"""
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"