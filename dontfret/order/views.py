"""
Title: order:views
Author: Ben Frame
Date: 10/04/2020
"""

# Imports
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderLine
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail  # For email confirmations
from dontfret.settings import EMAIL_HOST_USER


# Display a confirmation message once an order has been placed
def order_confirmed(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)  # Retrieve order with ID for display (or 404 error)
        email = request.user.email

        # Send confirmation email to customers saved email
        send_mail(
            'Don\'t Fret - Order Confirmation',  # Subject
            'Your order was successful! Please keep a note of your order number:\n' + str(order_id),  # Content
            EMAIL_HOST_USER,  # Email sender
            [email],  # Email reciever
            fail_silently=False,  # Raises exception should email fail
        )

    return render(request, 'order_confirmed.html', {'customer_order': customer_order})  # Display the order confirmed page with customer order details


# Display a confirmation message once an order has been placed
def order_refund_rejected(request, order_id):
    customer_order = get_object_or_404(Order, id=order_id)  # Retrieve order with ID for the order date (or 404 error)

    return render(request, 'order_refund_rejected.html', {'customer_order': customer_order})  # Display the order confirmed page with customer order details


# Display a confirmation message once an order has been placed
def order_refunded(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)  # Retrieve order with ID for display (or 404 error)

    return render(request, 'order_refunded.html', {'customer_order': customer_order})  # Display the order confirmed page with customer order details


@login_required()  # Anonymous users CANNOT access this page
def orderHistory(request):
    if request.user.is_authenticated:  # Check if user is registered
        email = str(request.user.email)  # Store their email in string
        order_details = Order.objects.filter(emailAddress=email)  # Retrieve order details from that customers email

    return render(request, 'order/orders_list.html', {'order_details': order_details})  # Display order list


@login_required()  # Anonymous users CANNOT access this page
def allOrderHistory(request):
    if request.user.is_staff:  # Only display all orders if the user is confirmed staff memeber
        order_details = Order.objects.all()  # Retrieve all orders

    return render(request, 'order/orders_list_all.html', {'order_details': order_details})  # Display order list


@login_required()  # Anonymous users CANNOT access this page
def viewOrder(request, order_id):
    if request.user.is_authenticated:  # Check if the user is logged in and has permission
        email = str(request.user.email)  # Retrieve email and store as string
        order = Order.objects.get(id=order_id, emailAddress=email)  # Retrieve order
        order_lines = OrderLine.objects.filter(order=order)  # Retrieve order lines of the order

    return render(request, 'order/order_detail.html', {'order': order, 'order_items': order_lines})  # Display order details with order lines


@login_required()  # Anonymous users CANNOT access this page
def refundOrder(request, order_id):
    if request.user.is_authenticated:  # Check if the user is logged in and has permission
        email = str(request.user.email)  # Retrieve email and store as string
        order = Order.objects.get(id=order_id)  # Retrieve order
        now = datetime.now().date()  # Establish exact date and time

        if now.day - order.order_date.day > 1:  # If the order is older than 24hrs then set is refundable to false
            return render(request, 'order_refund_rejected.html', {'order': order})  # Display the order refund rejected page as it has been longer than 24hrs
        else:
            order.is_refunded = True  # Mark order as refunded
            order.save()  # Save changes to order attributes (is_refunded)

            return render(request, 'order_refunded.html', {'order': order})  # Display the order refunded page

