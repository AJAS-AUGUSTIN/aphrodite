from django.urls import path
from . import views
urlpatterns = [

    path('',views.adminlogin, name = 'adminlogin'),
    path('adminhome/',views.adminhome, name= 'adminhome'),
    path('adminlogout/',views.adminlogout, name = 'adminlogout'),
    path('adminadduser/',views.adminadduser, name='adminadduser'),
    path('deluser/<int:id>',views.deluser, name='deluser'),
    path('updateuser/<int:id>',views.updateuser, name='updateuser'),
    path('statusupdate/<int:id>',views.statusupdate, name='statusupdate')
]
