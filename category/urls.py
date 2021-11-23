from django.urls import path
from .import views
from django.urls.resolvers import URLPattern

urlpatterns = [
    path('addproduct/',views.addproduct, name='addproduct'),
    path('Category/',views.Category, name='Category'),
    path('SubCategory/',views.SubCategory, name='SubCategory'),
    path('categoryhome/',views.categoryhome,name='categoryhome'),
    path('delcategory/<str:title>',views.delcategory,name='delcategory'),
    path('editcategory/<str:title>',views.editcategory,name='editcategory'),
    path('subcategoryhome/',views.subcategoryhome,name='subcategoryhome'),
    path('delsubcategory/<str:title>',views.delsubcategory,name='delsubcategory'),
    path('editsubcategory/<str:title>',views.editsubcategory,name='editsubcategory'),
    path('productshome/',views.productshome,name='productshome'),
    path('delproduct/<int:id>',views.delproduct,name='delproduct'),
    path('editproduct/<int:id>',views.editproduct,name='editproduct'),
    path('address/',views.address,name='address'),
    


]