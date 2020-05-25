"""
Title: cart:urls
Author: Ben Frame
Date: 09/04/2020
"""

# Imports
from django.urls import path
from . import views

app_name = 'cart'  # Sub-app cart is part of the dontfret project

# Various URLs that the website can go to to access the various apps/web pages within this project
urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name="add_cart"),  # Adding a particular product URL
    path('', views.cart_detail, name='cart_detail'),  # Viewing cart URL (main page of cart)
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),  # For decreasing quantity in cart
    path('full_remove/<int:product_id>/', views.full_remove, name='full_remove'),  # For binning item in cart
]