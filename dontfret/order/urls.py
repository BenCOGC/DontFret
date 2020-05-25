"""
Title: order:urls
Author: Ben Frame
Date: 10/04/2020
"""

# Imports
from django.urls import path
from . import views

app_name = 'order'  # Sub-program name

# Established the URL paths used in sub-program
urlpatterns = [
    path('order_confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),  # Page for displaying order confirmation
    path('order_refund_rejected/<int:order_id>/', views.order_refund_rejected, name='order_refund_rejected'),  # Page for displaying order refund rejected notification
    path('order_refunded/<int:order_id>/', views.order_refunded, name='order_refunded'),  # Page for displaying order refund confirmation
    path('refund_order/<int:order_id>/', views.refundOrder, name='refund_order'),  # Page for calculating viability of refund
    path('history/', views.orderHistory, name='order_history'),  # For viewing users previous orders
    path('all_orders/', views.allOrderHistory, name='all_order_history'),  # For Store Assistant to view all orders placed
    path('<int:order_id>/', views.viewOrder, name='order_detail'),  # For viewing order details of an order
]
