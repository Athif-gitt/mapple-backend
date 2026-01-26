from django.db import models
from django.contrib.auth.models import User
from products.models import Product  
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    ORDER_TYPE_CHOICES = (
        ('cart', 'Cart'),
        ('single', 'Single Product'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.CharField(
        max_length=10,
        choices=ORDER_TYPE_CHOICES,
        default='cart'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class OrderAddress(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery_address"
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)



    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
