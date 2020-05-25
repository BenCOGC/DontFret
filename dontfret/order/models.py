"""
Title: order:models
Author: Ben Frame
Date: 10/04/2020
"""

# Imports
from django.db import models
from django.core.validators import RegexValidator


# Order attributes
class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Order Total (£)')
    emailAddress = models.EmailField(max_length=250, verbose_name='Email Address')
    order_date = models.DateTimeField(auto_now_add=True)  # Date of when order created is auto-generated
    is_refunded = models.BooleanField(default=False)
    # Billing address details
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    # Shipping address details
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)
    # Payment Details (Regex Validator Used to Ensure Input is numerical)
    cardNo = models.CharField(max_length=16, default='0000000000000000', verbose_name='Card No.', validators=[RegexValidator(r'^\d{1,10}$')])
    #cardExpiryDate = models.CharField(max_length=4, default='0000', verbose_name='Card Expiry Date', validators=[RegexValidator(r'^\d{1,10}$')])
    #cardCCV = models.CharField(max_length=3, default='000', verbose_name='CCV No (Back Of Card)', validators=[RegexValidator(r'^\d{1,10}$')])

    # Additional options/details for model
    class Meta:
        db_table = 'Order'  # Save in a table called Order
        ordering = ['-order_date']  # Sort the table by the order date

    # Return as string
    def __str__(self):
        return str(self.id)  # Return order ID as string


# Order Line attributes
class OrderLine(models.Model):
    product = models.CharField(max_length=250)  # Name of product inside order
    quantity = models.IntegerField()  # The amount of that product purchased
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price (£)')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # When deleted remove all references in the order table

    # Additional options/details for model
    class Meta:
        db_table = 'OrderLine'  # Save in a table called OrderLine

    # Return sub-total that takes into account quantity purchased
    def sub_total(self):
        return self.quantity * self.price

    # Return as string
    def __str__(self):
        return self.product
