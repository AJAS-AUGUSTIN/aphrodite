from django.urls import path
from . import views
urlpatterns = [

    path('login/',views.login, name = 'login'),
    path('register/',views.register, name= 'register'),
    path('logout/',views.logout,name='logout'),
    path('',views.home,name='home'),
    path('otp/',views.otp, name='otp'),
    path('login_with_otp/',views.login_with_otp, name='login_with_otp'),
    path('check_otp/<str:phone_number>',views.check_otp, name='check_otp'),
    path('productdetails/<int:id>',views.productdetails,name='productdetails'),
    # path('cart/',views.cart,name='cart'),
    # path('update_item/',views.updateItem,name='update_item')
]