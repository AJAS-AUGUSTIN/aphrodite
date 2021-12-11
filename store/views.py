from django.http import HttpResponse
from django.core import paginator
from django.shortcuts import get_object_or_404, render

from category.models import Categories, SubCategories, Products
from category.views import Category
# from category.views import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store_q(request,subcategory_slug=None):
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

def store(request,category_slug=None):
    print("hii")
    print(category_slug)
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Categories,slug=category_slug)
        print(categories)
        products = Products.objects.filter(category=categories,is_available=True)
        print(products)
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:    
        products = Products.objects.all().filter(is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request, 'store/store.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by('-created_at').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
            print(products_count)
        context = {
            'products' : products,
            'products_count' : products_count
        }
    return render(request, 'store/store.html',context)

