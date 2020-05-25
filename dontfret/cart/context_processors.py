"""
Title: cart:context_processors
Author: Ben Frame
Date: 09/04/2020
"""

# Imports
from .models import Cart, CartItem
from .views import _cart_id


# Item counter
def counter(request):
    item_count = 0  # Initialise item_count to zero

    if 'admin' in request.path:  # If the user is an admin return nothing
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))  # Find specific cart
            cart_items = CartItem.objects.all().filter(cart=cart[:1])  # Get all items in specific cart

            for cart_item in cart_items:  # Count items in cart
                item_count += cart_item.quantity

        except Cart.DoesNotExist:  # If cart hasn't been made yet
            item_count = 0

    return dict(item_count=item_count)  # Return a dictionary of item_count
