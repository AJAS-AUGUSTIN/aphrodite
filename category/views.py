from django.shortcuts import render, redirect
from accounts.models import Account
import category
from category.models import Address, Categories, Products, SubCategories
from django.contrib import messages

# Create your views here.

def addproduct(request):
    categories = Categories.objects.all()
    subcategories = SubCategories.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        if Products.objects.filter(product_name=product_name):
             messages.error(
                request, "product already exists pls choose edit option")
             return redirect(addproduct)
        slug = product_name.replace(" ", "-").lower()
        brand = request.POST['brand']
        stock = request.POST['stock']
        product_max_price = request.POST['product_max_price']
        product_discount_price = request.POST['product_discount_price']
        product_description = request.POST['product_description']
        category_id = request.POST.get('Category')
        prod_instance = Categories.objects.get(id=category_id)
        SubCategories_id = request.POST['SubCategory']
        image1=request.FILES.get('image1')   
        product_instance =SubCategories.objects.get(id =SubCategories_id)
        Products.objects.create(product_name=product_name,url_slug=slug,brand=brand,stock=stock,product_max_price=product_max_price,product_discount_price=product_discount_price,product_description=product_description,SubCategories_id=product_instance,category=prod_instance,image1=image1)
        return redirect(addproduct)
        
    return render(request, 'addproducts.html',{'subcategories':subcategories,'categories':categories})

def Category(request):
    if request.method == 'POST':
        title = request.POST['title'].lower()
        if Categories.objects.filter(title=title):
            messages.error(
                request, "category already exists pls choose edit option")
            return redirect(Category)
        slug = title.replace(" ", "-").lower()
        description = request.POST['description']
        cat_image=request.FILES.get('cat_image')
        Categories.objects.create(title=title,slug=slug,description=description,cat_image=cat_image)
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
        url_slug = title.replace(" ", "-").lower()
        description = request.POST['description']
        category_id = request.POST['Category']
        cat_instance =Categories.objects.get(id =category_id)
        SubCategories.objects.create(title=title,url_slug=url_slug,description=description,category_id =cat_instance)
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
    return redirect(subcategoryhome)

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
        description = request.POST['description']

        if title != '':
            categories.title = title
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
        description = request.POST['description']

        if title != '':
            subcategories.title = title
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
        brand = request.POST['brand']
        product_max_price= request.POST['product_max_price']
        product_discount_price = request.POST['product_discount_price']
        product_description=request.POST['product_description']
        if product_name != '':
            products.product_name = product_name
        if brand != '':
            products.brand = brand
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

def add_address(request):
    current_user = request.user
    user = Account.objects.get(username=current_user)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        order_note  = request.POST['order_note']
        address = Address.objects.create(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,address_line_1=address_line_1,address_line_2=address_line_2,city=city,state=state,country=country,pincode=pincode,order_note=order_note,user_id=user)
        return redirect('listaddress')
    else:
        return render(request,'address.html')

