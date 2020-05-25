"""dontfret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView

"""
Title: dontfret:urls
Author: Ben Frame
Date: 06/04/2020
"""

# Imports
from django.contrib import admin
from django.urls import path, include
from DontFretShop import views
from django.conf import settings
from django.conf.urls.static import static  # Required for static About Us page

# Various URLs that the website can go to to access the various apps/web pages within this sub-program
urlpatterns = [
    path('admin/', admin.site.urls),  # URL location of admin features
    path('', views.index, name='index'),  # The index page
    path('DontFretShop/', include('DontFretShop.urls')),  # URL location of the shop
    path('search/', include('search_app.urls')),  # URL location of the search results
    path('cart/', include('cart.urls')),  # URL location of the cart
    path('order/', include('order.urls')),  # URL location of the order stats
    path('account/create/', views.signupView, name='signup'),  # URL location of the create account form
    path('account/create-store-assistant/', views.storeAssistantSignupView, name='signup-storeassistant'),  # URL location of the create store assistant form
    path('account/create-stock-controller/', views.stockControllerSignupView, name='signup-stockcontroller'),  # URL location of the create stock controller form
    path('account/edit-details/', views.editDetailsView, name='edit-details'),  # URL location of the edit account details form
    path('account/login/', views.signinView, name='signin'),  # URL location of the login page
    path('account/logout/', views.signoutView, name='signout'),  # URL for logging out
    path(r'^$', TemplateView.as_view(template_name="about-us.html"), name='about-us'),  # URL for the about us page
]

# If debugging mode is on then stored files are still available
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
