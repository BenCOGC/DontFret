"""
Title: cart:forms
Author: Ben Frame
Date: 09/04/2020
"""

# Imports
from django import forms
from order.models import Order
from django.core.validators import RegexValidator  # Form for creation of User (and also as a template for editing user details)


# Form for getting card details for a purchase
class CardPaymentForm(forms.Form):
    cardNo = forms.CharField\
        (max_length=16, default='0000000000000000', verbose_name='Card No.',validators=[RegexValidator(r'^\d{1,10}$')])
    cardExpiryDateMonth = forms.CharField\
        (max_length=2, default='00', verbose_name='Card Expiry Date', validators=[RegexValidator(r'^\d{1,10}$')])
    cardExpiryDateYear = forms.CharField\
        (max_length=4, default='0000', verbose_name='Card Expiry Date', validators=[RegexValidator(r'^\d{1,10}$')])
    cardCCV = forms.CharField\
        (max_length=3, default='000', verbose_name='CCV No (Back Of Card)', help_text='The last 3 numbers on the back of your card', validators=[RegexValidator(r'^\d{1,10}$')])

    class Meta:
        model = Order  # Save data as part of a User model (as part of Python/Django)
        fields = ('cardNo', 'cardExpiryDateMonth', 'cardExpiryDateYear', 'cardCCV')  # Create fields
