from django.shortcuts import render, redirect
import category
from category.models import Categories, Products, SubCategories
from django.contrib import messages

# Create your views here.

def addproduct(request):
    subcategories = SubCategories.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        if Products.objects.filter(product_name=product_name):
             messages.error(
                request, "product already exists pls choose edit option")
             return redirect(addproduct)
        url_slug = request.POST['url_slug']
        if Products.objects.filter(url_slug=url_slug):
            messages.error(
                request, "url_slug already exists pls choose edit option")
            return redirect(addproduct)
        brand = request.POST['brand']
        product_max_price = request.POST['product_max_price']
        product_discount_price = request.POST['product_discount_price']
        product_description = request.POST['product_description']
        SubCategories_id = request.POST['SubCategory']
        image1=request.FILES['image1']   
        product_instance =SubCategories.objects.get(id =SubCategories_id)
        Products.objects.create(product_name=product_name,url_slug=url_slug,brand=brand,product_max_price=product_max_price,product_discount_price=product_discount_price,product_description=product_description,SubCategories_id=product_instance,image1=image1)
        return redirect(addproduct)
        
    return render(request, 'addproducts.html',{'subcategories':subcategories})

def Category(request):
    if request.method == 'POST':
        title = request.POST['title']
        if Categories.objects.filter(title=title):
            messages.error(
                request, "category already exists pls choose edit option")
            return redirect(Category)
        url_slug = request.POST['url_slug']
        if Categories.objects.filter(url_slug=url_slug):
            messages.error(
                request, "category already exists pls choose edit option")
            return redirect(Category)
        thumbnail = request.POST['thumbnail']
        description = request.POST['description']
        Categories.objects.create(title=title,url_slug=url_slug,thumbnail=thumbnail,description=description)
        return redirect(Category)
    else:
        return render(request, 'addcategory.html')  

def SubCategory(request):
    categories = Categories.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        if SubCategories.objects.filter(title=title):
            messages.error(
                request, "SubCategory already exists pls choose edit option")
            return redirect(SubCategory)
        url_slug = request.POST['url_slug']
        if SubCategories.objects.filter(url_slug=url_slug):
            messages.error(
                request, "SubCategory already exists pls choose edit option")
            return redirect(SubCategory)
        thumbnail = request.POST['thumbnail']
        description = request.POST['description']
        category_id = request.POST['Category']
        cat_instance =Categories.objects.get(id =category_id)
        SubCategories.objects.create(title=title,url_slug=url_slug,thumbnail=thumbnail,description=description,category_id =cat_instance)
        return redirect(SubCategory)
    return render(request, 'subcategory.html',{'categories':categories} )


def categoryhome(request):
    categories = Categories.objects.all()
    return render(request, 'category.html',{'categories':categories})

def subcategoryhome(request):
    subcategories = SubCategories.objects.all()
    return render(request, 'subcategoryhome.html',{'subcategories':subcategories})

def productshome(request):
    products = Products.objects.all()
    return render(request, 'productshome.html',{'products':products})

def delcategory(request, title):
    try:
        categories = Categories.objects.get(title=title)
        categories.delete()
        messages.sucess(request, "The category is deleted")
    except:
        messages.error(request, "The category not found")
    return redirect(categoryhome)

def delsubcategory(request, title):
    try:
        subcategories = SubCategories.objects.get(title=title)
        subcategories.delete()
        messages.sucess(request, "The category is deleted")
    except:
        messages.error(request, "The category not found")
    return redirect(categoryhome)

def delproduct(request, id):
    try:
        products = Products.objects.get(id=id)
        products.delete()
        messages.sucess(request, "The product is deleted")
    except:
        messages.error(request, "The product not found")
    return redirect(productshome)


def editcategory(request, title):
    categories = Categories.objects.get(title=title)
    if request.method == 'POST':
        title = request.POST['title']
        url_slug = request.POST['url_slug']
        thumbnail = request.POST['thumbnail']
        description = request.POST['description']

        if title != '':
            categories.title = title
        if thumbnail != '':
            categories.thumbnail = thumbnail
        if url_slug != '':
            categories.url_slug = url_slug
        if description != '':
            categories.description = description
            categories.save()
            return redirect(categoryhome)
    else:
        return render(request, 'editcategory.html',{'category':categories})

def editsubcategory(request, title):
    categories = Categories.objects.all()
    subcategories = SubCategories.objects.get(title=title)
    if request.method == 'POST':
        title = request.POST['title']
        url_slug = request.POST['url_slug']
        thumbnail = request.POST['thumbnail']
        description = request.POST['description']

        if title != '':
            subcategories.title = title
        if thumbnail != '':
            subcategories.thumbnail = thumbnail
        if url_slug != '':
            subcategories.url_slug = url_slug
        if description != '':
            subcategories.description = description
            subcategories.save()
            return redirect(subcategoryhome)
    else:
        return render(request, 'editsubcategory.html',{'subcategory':subcategories,'categories':categories})

def editproduct(request, id):
    products = Products.objects.get(id=id)
    subcategories = SubCategories.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        url_slug = request.POST['url_slug']
        brand = request.POST['brand']
        product_max_price= request.POST['product_max_price']
        product_discount_price = request.POST['product_discount_price']
        product_description=request.POST['product_description']
        if product_name != '':
            products.product_name = product_name
        if brand != '':
            products.brand = brand
        if url_slug != '':
            products.url_slug = url_slug
        if product_description != '':
            products.product_description = product_description
        if product_max_price != '':
            products.product_max_price = product_max_price
        if product_discount_price != '':
            products.product_discount_price = product_discount_price
            products.save()
            return redirect(productshome)
    else:
        return render(request, 'editproducts.html',{'product':products,'subcategories':subcategories})

def address(request):
    return render(request, 'address.html')

