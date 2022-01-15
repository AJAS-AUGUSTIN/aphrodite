from django.urls import path

from aphrodite import views
from .import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('final/',views.final,name='final'),
    path('place_order/',views.place_order,name='place_order'),
    path('paypal_payment/',views.paypal_payment,name='paypal_payment'),
    path('paypal_payment_success/',views.paypal_payment_success,name='paypal_payment_success'),
    path('payment_error/',views.payment_error,name='payment_error'),
    path('razor_pay_details/',views.razor_pay_details,name='razor_pay_details'),
    path('buy_now/<int:id>/',views.buy_now,name='buy_now'),
    path('add_wishlist/',views.add_wishlist,name='add_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wish_item/',views.remove_wish_item, name='remove_wish_item'),
    path('cart_inc/<int:id>/',views.cart_inc,name='cart_inc'),
    
]