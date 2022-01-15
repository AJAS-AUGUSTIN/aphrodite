from django.core.checks import messages
from django.http import HttpResponse
from django.core import paginator
from django.shortcuts import get_object_or_404, render
from category.models import Brand, Categories, SubCategories, Products
from category.views import Category
# from category.views import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from category.models import Brand
from store.models import Banner
from django.contrib import messages


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
    brand=Brand.objects.all()
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Categories,slug=category_slug)
        products = Products.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:    
        products = Products.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        'products':paged_products,
        'products_count':products_count,
        'brand':brand
    }
    return render(request, 'store/store.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by('-created_at').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
        context = {
            'products' : products,
            'products_count' : products_count
        }
    return render(request, 'store/store.html',context)


def add_banner(request):
    if request.method == 'POST':
        image1=request.FILES.get('image1')
        try:
            banner = Banner.objects.create(image1=image1)
            messages.success(request, 'Image added')
        except:
            messages.error(request, 'Image not added.')
    return render(request, 'add_banner.html')

