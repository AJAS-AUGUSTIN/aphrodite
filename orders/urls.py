from os import name
from django.urls import path
from . import views
from django.urls.resolvers import URLPattern

urlpatterns = [
    path('',views.orders,name='orders'),
    path('editordersadmin/<int:id>',views.editordersadmin,name='editordersadmin'),
    path('statuschange/<int:id>',views.statuschange,name='statuschange'),
    path('sales_report/',views.sales_report,name='sales_report'),
]