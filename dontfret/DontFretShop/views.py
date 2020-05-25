"""
Title: DontFretShop:views
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


# The index page is the first page that loads
def index(request):
	return redirect('DontFretShop:featuredProdCat')  # Navigate to the main menu


# View of all products
def allProdCat(request, c_slug=None):
	# Initialise variables
	c_page = None
	products_list = None

	# Gather list of products in category
	if c_slug == 'featured':
		products_list = Product.objects.filter(is_featured=True)
	if c_slug!=None:  # A specific category is selected
		c_page = get_object_or_404(Category, slug=c_slug)
		products_list = Product.objects.filter(category=c_page, is_available=True)
	else:  # All Products is selected (default)
		products_list = Product.objects.all().filter(is_available=True)

	# Paginator - For managing layout
	paginator = Paginator(products_list, 6)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage, InvalidPage):
		products = paginator.page(paginator.num_pages)
	# /Paginator

	return render(request, 'DontFretShop/category.html', {'category': c_page, 'products': products})


# View of all featured products
def featuredProdCat(request, c_slug=None):
	# Initialise variables
	c_page = None

	# Gather list of featured products
	products_list = Product.objects.filter(is_featured=True)

	# Paginator - For managing layout
	paginator = Paginator(products_list, 6)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage, InvalidPage):
		products = paginator.page(paginator.num_pages)
	# /Paginator

	return render(request, 'DontFretShop/category.html', {'category': c_page, 'products': products})


# When you click on a particular product
def ProdCatDetail(request, c_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug, slug=product_slug)  # Retrieve selected product
	except Exception as ex:
		raise ex  # Display error

	return render(request, 'DontFretShop/product.html', {'product': product})  # Display specific product page


# For new customers signing up for an account
def signupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)  # Retrieve details from filled form

		if form.is_valid():
			form.username = form.cleaned_data.get('email')  # Set the username to email (this is a workaround so I can use the default User model without errors [ideally I would have used a different model from the start])
			user = form.save()  # Save the form

			if user is not None:
				user.save()
				username = form.cleaned_data.get('username')  # Get users username for ID
				#email = form.cleaned_data.get('email')  # Get users email for ID
				signup_user = User.objects.get(username=username)  # Keep the email identifier of the user signing up
				customer_group = Group.objects.get(name='Customer')  # Find the Customer group of users
				customer_group.user_set.add(signup_user)  # Add the user to the group

				login(request, user)  # Once user has registered log them in
				return redirect('DontFretShop:featuredProdCat')  # Redirect them to the main menu
			else:
				return redirect('signup')  # Unsuccessful, reload page
	else:
		form = SignUpForm()  # Display the sign up form again

	return render(request, 'accounts/signup.html', {'form': form})  # Go to signup page with form details


# For new stock controllers signing up for an account
def stockControllerSignupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)  # Retrieve details from filled form

		if form.is_valid():
			user = form.save()  # Save the form

			if user is not None:
				user.is_staff = True  # Give new staff member staff permissions
				user.save()  # Save changes to permissions
				username = form.cleaned_data.get('username')  # Get users username for ID
				signup_user = User.objects.get(username=username)  # Keep the email identifier of the user signing up
				staff_group = Group.objects.get(name='Stock Controller')  # Find the Customer group of users
				staff_group.user_set.add(signup_user)  # Add the user to the group

				login(request, user)  # Once user has registered log them in
				return redirect('DontFretShop:featuredProdCat')  # Redirect them to the main menu
			else:
				return redirect('signup')  # Unsuccessful, reload page
	else:
		form = SignUpForm()  # Display the sign up form again

	return render(request, 'accounts/signup-stockcontroller.html', {'form': form})  # Go to signup page with form details


# For new stock controllers signing up for an account
def storeAssistantSignupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)  # Retrieve details from filled form

		if form.is_valid():
			user = form.save()  # Save the form

			if user is not None:
				user.is_staff = True  # Allows stock controller to access the admin permissions of their group
				user.save()  # Save changes to permissions
				username = form.cleaned_data.get('username')  # Get users username for ID
				signup_user = User.objects.get(username=username)  # Keep the email identifier of the user signing up
				staff_group = Group.objects.get(name='Store Assistant')  # Find the Customer group of users
				staff_group.user_set.add(signup_user)  # Add the user to the group

				login(request, user)  # Once user has registered log them in
				return redirect('DontFretShop:featuredProdCat')  # Redirect them to the main menu
			else:
				return redirect('signup')  # Unsuccessful, reload page
	else:
		form = SignUpForm()  # Display the sign up form again

	return render(request, 'accounts/signup-storeassistant.html', {'form': form})  # Go to signup page with form details


# Sign in user by requesting they fill out their username and password
def signinView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)  # Retrieve details from input login credentials

		if form.is_valid():  # If login credentials are filled in (regardless if they are correct)
			username = request.POST['username']  # Retrieve input username
			password = request.POST['password']  # Retrieve input password
			user = authenticate(username=username, password=password)  # Try to find a match for the input credentials

			if user is not None:  # A match has been found for the user trying to login
				login(request, user)  # User is now logged in for that session unless they sign out

				return redirect('DontFretShop:featuredProdCat')  # Navigate to the main menu
			else:  # No match was found for the user trying to login
				return redirect('signup')  # Redirect to the sign up page
	else:
		form = AuthenticationForm()  # Not all fields filled in, reload form

	return render(request, 'accounts/signin.html', {'form': form})


# Sign out currently logged in user
def signoutView(request):
	logout(request)  # Request user be logged out

	return redirect('signin')  # Redirect to sign in page


def editDetailsView(request):
	user = request.user  # Retrieve and store users details
	form = SignUpForm(request.POST or None, initial={
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name})  # Save all to form variable (and auto-fill the form with user data using initial)

	if request.method == 'POST':

		if form.is_valid():  # If user input can be accepted

			# Change locally stored user details to their updated versions
			user.email = request.POST['email']
			#user.username = request.POST['email']  # A users username IS their email (a workaround so I can still use the default User model Python/Django provides)
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.set_password(request.POST['password1'])

			User = user  # Local user is the same as global User
			User.save()  # Save the changes to logged in User's details

			return redirect('DontFretShop:featuredProdCat')  # Redirect them to the main menu
	else:
		form = SignUpForm(initial={
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name})  # Display the sign up form again (auto-fill details again)

	return render(request, 'accounts/edit-details.html', {'form': form})  # Go to edit details page with form details