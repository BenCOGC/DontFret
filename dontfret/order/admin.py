"""
Title: order:admin
Author: Ben Frame
Date: 10/04/2020
"""

# Imports
from django.contrib import admin
from .models import Order, OrderLine
from datetime import datetime


# Configure settings for admin manipulating order lines (can only view)
class OrderLineAdmin(admin.TabularInline):
    model = OrderLine
    fieldsets = [
        ('Product', {'fields': ['product'], }),
        ('Quantity', {'fields': ['quantity'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False  # Makes admin unable to delete individual order lines
    max_num = 0  # Fixes blank order lines showing up
    template = 'admin/order/tabular.html'  # Use this particular template for display


@admin.register(Order)  # Register model Order in admin section
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'emailAddress', 'order_date', 'is_refunded']  # Order details displayed
    list_display_links = ('id', 'billingName')  # Order details that can be clicked on for more information
    search_fields = ['id', 'billingName', 'emailAddress']  # Search for order by ID, billing name or email address
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'order_date',  # Detailed invoice of an order (read-only)
                       'billingName', 'billingAddress1', 'billingCity', 'billingPostcode', 'billingCountry',
                       'shippingAddress1', 'shippingCity', 'shippingPostcode', 'shippingCountry']
    fieldsets = [  # Display these tables with the following data
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'order_date', 'is_refunded']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1', 'billingCity', 'billingPostcode', 'billingCountry']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1', 'shippingCity', 'shippingPostcode', 'shippingCountry']}),
    ]

    inlines = [
        OrderLineAdmin,
    ]

    def has_delete_permission(self, request, obj=None):  # Disables delete button (not within Store Assistant scope)
        return False

    def has_add_permission(self, request):  # Disables add button (not within Store Assistant scope)
        return False

    def has_change_permission(self, request, obj=None):  # Disables change permissions as there is a dedicated page for refunds
        return False