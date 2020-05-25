"""
Title: DontFretShop:context_processors
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from .models import Category


# Populate dropdown menu with links to all the different categories
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
