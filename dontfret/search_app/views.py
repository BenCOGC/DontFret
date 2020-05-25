"""
Title: search_app:views
Author: Ben Frame
Date: 07/04/2020
"""

# Imports
from django.shortcuts import render
from DontFretShop.models import Product
from django.db.models import Q


# Search bar functionality
def searchResult(request):
    # Initialise variables
    products = None
    query = None

    if 'q' in request.GET:
        query = request.GET.get('q')  # Store query made by user
        # Return results if search keywords are found in either the product name or product description
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))

    return render(request, 'search.html', {'query': query, 'products': products})  # Render the search results page
