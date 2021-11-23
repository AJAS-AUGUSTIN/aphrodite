from django.urls import path

from aphrodite import views
from .import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('final/',views.final,name='final'),
    path('place_order',views.place_order,name='place_order'),
]