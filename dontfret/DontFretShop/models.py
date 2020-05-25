"""
Title: DontFretShop:models
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django.db import models
from django.urls import reverse


# Determines attributes for the Category model
class Category(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category', blank=True)

	# Additional options/details for model
	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	# Gets url for specific category
	def get_url(self):
		return reverse('DontFretShop:products_by_category', args=[self.slug])

	# Return as string
	def __str__(self):
		return '{}'.format(self.name)


# Determines attributes for the Product model
class Product(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)  # Products unique URL
	brand = models.CharField(max_length=250, unique=False, default='Don\'t Fret Brand')  # Brand name defaults to the Don't Fret Brand if not given one
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)  # If product is deleted any other references are deleted too!
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='product', blank=True)
	stock = models.IntegerField()
	is_available = models.BooleanField(default=True)  # Available by default when created
	release_date = models.DateTimeField(auto_now_add=True)  # Store date of when product was first available
	updated_date = models.DateTimeField(auto_now=True)  # Store date of when product was last updated
	is_featured = models.BooleanField(default=False)  # Determines whether product is displayed in the featured section

	# Additional options/details for model
	class Meta:
		ordering = ('name',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	# Gets url for specific product
	def get_url(self):
		return reverse('DontFretShop:ProdCatDetail', args=[self.category.slug, self.slug])

	# Return as string
	def __str__(self):
		return '{}'.format(self.name)
