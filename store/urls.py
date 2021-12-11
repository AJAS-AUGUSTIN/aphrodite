from django.urls import path
from .import views
from django.urls.resolvers import URLPattern
from users.views import productdetails
from .import views

urlpatterns = [
    path('',views.store, name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    # path('category/<slug:category_slug>/<slug:product_slug>/',views.productdetails,name='productdetails'),
    # path('<slug:subcategory_slug>',views.store,name='products_by_subcategory'),
    path('search/',views.search,name='search'),


    
    # do product slug
    


]