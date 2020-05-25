"""
Title: DontFretShop:urls
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django.urls import path
from . import views

app_name = 'DontFretShop'  # Sub-program name

# Various URLs that the website can go to to access the various apps/web pages within this sub-program
urlpatterns = [
	path('', views.featuredProdCat, name='featuredProdCat'),  # The featured products page (the main menu/home page)
	path('all/', views.allProdCat, name='allProdCat'),  # The all products page
	path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),  # The category page which has a URL based on its slug
	path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name='ProdCatDetail'),  # The product details page
]
