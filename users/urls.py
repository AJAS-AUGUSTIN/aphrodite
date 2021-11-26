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
    path('userdetails/',views.userdetails,name='userdetails'),
    path('editaddress/<int:id>/',views.editaddress,name='editaddress'),
    path('listaddress/',views.listaddress,name='listaddress'),
    path('deleteaddress/<int:id>',views.deleteaddress,name='deleteaddress'),
    path('add_address_checkout/',views.add_address_checkout,name='add_address_checkout'),
    path('change_password/',views.change_password,name='change_password'),
    path('account_details/',views.account_details,name='account_details'),
    # path('change_password_user/<int:id>',views.change_password_user, name='change_password_user')
    # path('save_address',views.save_address,name='save_address'),
]