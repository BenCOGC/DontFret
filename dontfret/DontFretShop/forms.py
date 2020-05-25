"""
Title: DontFretShop:forms
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Form for creation of User (and also as a template for editing user details)
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='e.g. yourname@email.com')

    class Meta:
        model = User  # Save data as part of a User model (as part of Python/Django)
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')  # Create fields
