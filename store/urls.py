from django.urls import path
from .import views
from django.urls.resolvers import URLPattern

urlpatterns = [
    path('',views.store, name='store'),
    path('<slug:subcategory_slug>',views.store,name='products_by_subcategory'),
    # path('<slug:category_slug>',views.store_q,name='products_by_category'),
    


]