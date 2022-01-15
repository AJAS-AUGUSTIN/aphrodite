
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