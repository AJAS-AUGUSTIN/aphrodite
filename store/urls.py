from django.urls import path
from .import views
from django.urls.resolvers import URLPattern
from users.views import productdetails
from .import views

urlpatterns = [
    path('',views.store, name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('search/',views.search,name='search'),
    path('add_banner/',views.add_banner,name='add_banner'),
    
]