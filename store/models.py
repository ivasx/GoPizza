from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Product Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Category")
    available = models.BooleanField(default=True, verbose_name="Available")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        """Calculate total price of items in cart"""
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Calculate cost of this cart item"""
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Confirmation'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="User")
    address = models.CharField(max_length=250, verbose_name="Delivery Address")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_cost(self):
        """Calculate total cost of order"""
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Calculate cost of this order item"""
        return self.price * self.quantity

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"