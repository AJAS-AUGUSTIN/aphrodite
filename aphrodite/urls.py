"""aphrodite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from category.views import Category
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('accounts.urls')),
    path('',views.home, name='home'),
    path('', include('users.urls')),
    path('admin/',include('category.urls')),
    path('cart/',include('carts.urls')),

    #orders
    path('orders/',include('orders.urls')),
    path('store/',include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)