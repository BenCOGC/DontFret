"""
Title: search_app:urls
Author: Ben Frame
Date: 07/04/2020
"""

# Imports
from django.urls import path
from . import views


app_name = 'search_app'  # Sub-program name


# Established the URL paths used in sub-program
urlpatterns = [
    path('', views.searchResult, name='searchResult')  # The results url (main and only search URL)
]
