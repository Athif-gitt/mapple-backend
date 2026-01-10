from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['wishlist', 'product']
