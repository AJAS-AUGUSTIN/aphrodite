from django.urls import path
from . import views
urlpatterns = [

    path('',views.adminlogin, name = 'adminlogin'),
    path('adminhome/',views.adminhome, name= 'adminhome'),
    path('adminlogout/',views.adminlogout, name = 'adminlogout'),
    path('deluser/<int:id>',views.deluser, name='deluser'),
    path('updateuser/<int:id>',views.updateuser, name='updateuser'),
    path('statusupdate/<int:id>',views.statusupdate, name='statusupdate'),
    path('pdf_report/',views.pdf_report,name='pdf_report'),
    
]
