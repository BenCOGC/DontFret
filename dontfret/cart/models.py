"""
Title: cart:models
Author: Ben Frame
Date: 09/04/2020
"""

# Imports
from django.db import models
from DontFretShop.models import Product


# Determines attributes for Cart model
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    # Additional options/details for model
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    # Return as string
    def __str__(self):
        return self.cart_id


# Determines attributes for Cart Item model (individual products in cart)
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    # Additional options/details for model
    class Meta:
        db_table = 'CartItem'

    # Calculate sub total
    def sub_total(self):
        return self.product.price * self.quantity

    # Return as string
    def __str__(self):
        return self.product
