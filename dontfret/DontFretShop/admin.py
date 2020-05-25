"""
Title: DontFretShop:admin
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django.contrib import admin
from .models import Category, Product


# The following states the types of admins allowed in this system and what permissions they have
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']  # The fields
	prepopulated_fields = {'slug': ('name',)}  # Auto generate a slug


admin.site.register(Category, CategoryAdmin)  # Register new admin


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'brand', 'category', 'price', 'stock', 'is_available', 'release_date', 'updated_date', 'is_featured']  # Product fields
	list_editable = ['price', 'stock', 'is_available', 'is_featured']  # Fields that can be edited after being created
	prepopulated_fields = {'slug': ('name',)}  # Prepopulate the slug field based on what is contained inside the name field
	list_per_page = 20  # Amount of entries that can fit on one page


admin.site.register(Product, ProductAdmin)  # Register new admin
