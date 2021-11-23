from os import name
from django.urls import path
from . import views
from django.urls.resolvers import URLPattern

urlpatterns = [
    path('',views.orders,name='orders')
    # path('place_order',views.place_order,name='place_order'),
]