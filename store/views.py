from re import T
from django.shortcuts import get_object_or_404, render

from category.models import Categories, SubCategories, Products
from category.views import Category
# from category.views import Category

# Create your views here.
def store(request,subcategory_slug=None):
    subcategories = None
    products = None
    if subcategory_slug != None:
        subcategories = get_object_or_404(SubCategories ,url_slug=subcategory_slug)
        products = Products.objects.filter(SubCategories_id = subcategories,is_available=True)
        products_count = products.count()
    else:    
        products = Products.objects.all().filter(is_available=True)
        products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/store.html',context)

def store_q(request,category_slug=None):
    print("hii")
    print(category_slug)
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Categories,slug=category_slug)
        print(categories)
        products = Products.objects.filter(category=categories,is_available=True)
        print(products)
        products_count = products.count()
    else:    
        products = Products.objects.all().filter(is_available=True)
        products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/store.html',context)