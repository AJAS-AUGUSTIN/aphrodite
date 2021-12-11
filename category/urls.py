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
    path('add_address/',views.add_address,name='add_address'),
    path('add_offer/',views.add_offer,name='add_offer'),
    path('view_offer/',views.view_offer,name='view_offer'),
    path('edit_offer/<int:id>',views.edit_offer,name='edit_offer'),
    path('delete_offer/<int:id>',views.delete_offer,name='delete_offer'),

    path('add_category_offer/',views.add_category_offer,name='add_category_offer'),
    path('delete_category_offer/<int:id>',views.delete_category_offer,name='delete_category_offer'),

    path('add_product_offer/',views.add_product_offer,name='add_product_offer'),
    


]