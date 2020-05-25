"""
Title: cart:views
Author: Ben Frame
Date: 09/04/2020
"""

# Imports
from django.contrib.auth.models import Permission, User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from dontfret.settings import EMAIL_HOST_USER
from DontFretShop.models import Product
from . models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from order.models import Order, OrderLine


def _cart_id(request):
    cart = request.session.session_key  # Request the id of the cart particular to the current session (if there is one)

    if not cart:  # If there is no cart in the current session
        cart = request.session.create()

    return cart  # Return cart id


# Add product to cart (Add To Cart Button/Plus Button)
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get selected item to be added to cart

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # If a cart has already been established get cart ID
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)  # If a cart has not yet been established create one and get its ID
        )
        cart.save()  # Save the new cart

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)  # Get the item being added to cart

        if cart_item.quantity < cart_item.product.stock:  # Checks if there is enough stock to add to basket
            cart_item.quantity += 1  # Adds product to cart or increases the number of the same product in the cart

        cart_item.save()  # Save changes (if any) to cart
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()  # Save changes to cart

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Find the right cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)  # Get the items in the cart

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price for each product
            counter += cart_item.quantity  # Calculate quantity of product(s)
    except ObjectDoesNotExist:  # Cart does not exist
        pass

    # Stripe Pay By Card functionality
    stripe.api_key = settings.STRIPE_SECRET_KEY  # My personal api key for my stripe account as found in settings.py
    stripe_total = int(total * 100)
    description = 'Don\'t Fret - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY  # My personal api key for my stripe account as found in settings.py

    if request.method == 'POST':
        try:  # Retrieve data from Stripe payment form
            token = request.POST['stripeToken']  # Retrieve payment token
            email = request.user.email  # Retrieve paying users email from account NOT form

            # Retrieve billing details
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            # Retrieve shipping details
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            customer = stripe.Customer.create(  # Create customer with the retrieved info from Stripe payment form
                email=email,
                source=token
            )
            charge = stripe.Charge.create(  # Retrieve payment details
                amount=stripe_total,
                currency="gbp",
                description=description,
                customer=customer.id
            )

            # Creating the order
            try:
                order_details = Order.objects.create(  # Save the retrieved data to the order
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )

                order_details.save()  # Save changes to order now details have been added

                for order_line in cart_items:  # Retrieve order line details for each order line in order
                    ol = OrderLine.objects.create(
                        product=order_line.product.name,
                        quantity=order_line.quantity,
                        price=order_line.product.price,
                        order=order_details
                    )

                    ol.save()  # Save changes to order line each time an order line is added

                    # Reduce stock to reflect what has been purchased in the order
                    products = Product.objects.get(id=order_line.product.id)
                    products.stock = int(order_line.product.stock - order_line.quantity)  # Subtract ordered product from stock count
                    products.save()  # Save changes to stock levels
                    order_line.delete()

                    if products.stock < 4:  # Low stock warning if product has 3 or less left

                        # Gather the recipients list (all Stock Controllers)
                        users = User.objects.filter(groups__name='Stock Controller').values_list('email', flat=True)  # Retrieve all Stock Controller
                        recipients = list(users)  # Store them in a list of recipients

                        # Send each stock controller in list a low stock alert email
                        for email in recipients:
                            send_mail(
                                'Don\'t Fret - STOCK LOW',  # Subject
                                'Low stock warning for: ' + str(products),  # Content
                                EMAIL_HOST_USER,  # Email sender
                                [email],  # Email reciever
                                fail_silently=False,  # Raise exception if email fails
                            )

                    print('Your order has been placed!')  # Confirmation message in console (for debugging)

                return redirect('order:order_confirmed', order_details.id)  # Redirect to order confirmation page

            except ObjectDoesNotExist:  # Error
                pass

        except stripe.error.CardError as e:  # An error has occurred
            return False, e
    # /Stripe Pay By Card functionality

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter,  # Display populated cart
                                             data_key=data_key, stripe_total=stripe_total, description=description))


# Reduce item quantity from cart (minus button)
def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the user cart
    product = get_object_or_404(Product, id=product_id)  # Find the product to remove (else 404 error)
    cart_item = CartItem.objects.get(product=product, cart=cart)  # Find the specific item in cart based on the user cart and specific product

    if cart_item.quantity > 1:  # If the quantity is greater than one then simply decrease the quantity by one
        cart_item.quantity -= 1
        cart_item.save()  # Save changes
    else:
        cart_item.delete()  # Item already has quantity of one so remove item from cart entirely

    return redirect('cart:cart_detail')  # Return changes


# Fully remove item from cart regardless of quantity (bin button)
def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the user cart
    product = get_object_or_404(Product, id=product_id)  # Find the product to remove (else 404 error)
    cart_item = CartItem.objects.get(product=product, cart=cart)  # Find the specific item in cart based on the user cart and specific product
    cart_item.delete()  # Remove item from cart regardless of quantity

    return redirect('cart:cart_detail')  # Return changes

