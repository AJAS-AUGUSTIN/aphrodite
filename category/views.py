from django.http import request
from django.shortcuts import render, redirect
from accounts.models import Account
import category
from category.models import Address, Categories, Coupon, Offer, Products, SubCategories
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from carts.models import CartItems,Cart
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
        # image1=request.FILES.get('image1')
        
        #for cropping
        image1 = request.POST.get('pro_img1')
        print("hiiiiiiiiii",image1)
        image2 = request.POST.get('pro_img2')
        image3 = request.POST.get('pro_img3')
        image4 = request.POST.get('pro_img4')

        format, img1 = image1.split(';base64,')
        ext = format.split('/')[-1]
        product_image1 = ContentFile(base64.b64decode(img1), name= product_name + '1.' + ext)
        
        
        format, img2 = image2.split(';base64,')
        ext = format.split('/')[-1]
        product_image2 = ContentFile(base64.b64decode(img2), name= product_name + '2.' + ext)
        
        format, img3 = image3.split(';base64,')
        ext = format.split('/')[-1]
        product_image3 = ContentFile(base64.b64decode(img3), name= product_name + '3.' + ext)
        
        format, img4 = image4.split(';base64,')
        ext = format.split('/')[-1]
        product_image4 = ContentFile(base64.b64decode(img4), name= product_name + '4.' + ext)
        


        product_instance =SubCategories.objects.get(id =SubCategories_id)
        Products.objects.create(product_name=product_name,url_slug=slug,brand=brand,stock=stock,product_max_price=product_max_price,product_discount_price=product_discount_price,product_description=product_description,SubCategories_id=product_instance,category=prod_instance,image1=product_image1,image2=product_image2,image3=product_image3,image4=product_image4)
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
        stock = request.POST['stock']
        product_max_price= request.POST['product_max_price']
        product_discount_price = request.POST['product_discount_price']
        product_description=request.POST['product_description']
        if product_name != '':
            products.product_name = product_name
        if brand != '':
            products.brand = brand
        if stock != '':
            products.stock = stock
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

def add_offer(request):
    if request.method == 'POST':
        offer_name      = request.POST['offer_name']
        offer_percent   = request.POST['offer_percent']
        expiry_date     = request.POST['expiry_date']
        expiry_time     = request.POST['expiry_time']
        
        offer = Offer.objects.create(offer_name=offer_name,offer_percent=offer_percent,expiry_date=expiry_date,expiry_time=expiry_time)
    else:
        return render(request,'add_offer.html')
    return render(request,'add_offer.html')

def view_offer(request):
    offers = Offer.objects.all()
    return render(request,'view_offer.html',{'offers':offers})

def edit_offer(request,id):
    offers = Offer.objects.get(id=id)
    if request.method == 'POST':
        offers.offer_name      = request.POST['offer_name']
        offers.offer_percent   = request.POST['offer_percent']
        offers.expiry_date     = request.POST['expiry_date']
        offers.expiry_time     = request.POST['expiry_time']
        offers.save()
        return redirect('view_offer')  
    else:
        return render(request,'edit_offer.html',{'offers':offers})

def delete_offer(request,id):
    try:
        offers = Offer.objects.get(id=id)
        offers.delete()
        messages.sucess(request, "The offer is deleted")
    except:
        messages.error(request, "The offer not found")
    return redirect('view_offer')
    
def add_category_offer(request):
    categories = Categories.objects.all()
    offers = Offer.objects.all()
    category_offer = "category offer"
    context = {
        'offers':offers,
        'categories':categories
    }
    if request.method == 'POST':
        category_id = request.POST['hidden_category_id']
        categories = Categories.objects.get(id = category_id)
        offer = request.POST.get('offer')
        print(offer)
        try:
            if offer != 'none':
                offers = Offer.objects.get(offer_name = offer)
                offer_name = offers.offer_name
                categories.offer_name = offer_name
                categories.save()

                products = Products.objects.filter(category = category_id)
                for product in products:
                    product.offer_type = category_offer
                    product.offer_name = offers.offer_name           
                    product.offer_percent = offers.offer_percent         
                    product.expiry_date = offers.expiry_date         
                    product.expiry_time = offers.expiry_time
                    product.product_new_price = product.product_discount_price
                    product.product_discount_price =  product.product_discount_price-((product.product_discount_price*product.offer_percent)/100)
                    product.save()
                return redirect('add_category_offer')
            else:
                categories.offer_name = 'none'
                categories.save()
                
                
                products = Products.objects.filter(category = category_id)
                for product in products:
                    product.offer_type = None
                    product.offer_name = None          
                    product.offer_percent = None        
                    product.expiry_date = None      
                    product.expiry_time = None
                    product.product_discount_price = product.product_new_price
                    product.product_new_price = None
                    product.save()
                return redirect('add_category_offer')
        except:
            return redirect('add_category_offer')

        
    elif request.method == 'GET':
        return render(request,'add_category_offer.html',context)

def delete_category_offer(request,id):
    # category_id = request.POST.get('hidden_category_id')
    # print(category_id)
    # categories = Categories.objects.get(id = category_id)
    offers = Offer.objects.get(id = id)
    offers.delete()
    return render(request,'add_category_offer.html')


def add_product_offer(request):
    categories = Categories.objects.all()
    products = Products.objects.all()
    offers = Offer.objects.all()
    category_id = request.POST.get('hidden_category_id')
    context = {
        'products':products,
        'offers':offers,
    }
    if request.method == 'POST':
        product_id = request.POST['hidden_product_id']
        print(product_id)
        offer = request.POST.get('offer')
        print(offer)
        if offer != 'none':
            offers = Offer.objects.get(offer_name = offer)
            offer_name = offers.offer_name

            products = Products.objects.get(id = product_id)
            print(products.offer_percent)
            print(offers.offer_percent)
            if products.offer_percent < offers.offer_percent:
                products.offer_type = "product_offer"
                products.offer_name = offers.offer_name           
                products.offer_percent = offers.offer_percent         
                products.expiry_date = offers.expiry_date         
                products.expiry_time = offers.expiry_time
                products.save()
                return redirect('add_product_offer')
            else:
                category = Categories.objects.get(id = category_id)
                products.offer_type = "category offer"
                products.offer_name = category.offer_name         
                products.offer_percent = offers.offer_percent        
                products.expiry_date = offers.expiry_date
                products.expiry_time = offers.expiry_time
                products.save()
                return redirect('add_product_offer')
        else:                                       
            products = Products.objects.get(id = product_id)
            offer_name = products.category.offer_name
            print(products)
            print(offer_name)
            category = Categories.objects.get(id = category_id)
            print(category.offer_name)
            try:
                offer = Offer.objects.get(offer_name=category.offer_name)
                if offer_name:
                    products.offer_type = "category offer"
                    products.offer_name = category.offer_name         
                    products.offer_percent = offer.offer_percent        
                    products.expiry_date = offer.expiry_date
                    products.expiry_time = offer.expiry_time
                    products.save()
                    return redirect('add_product_offer')
                else:
                    pass
            except:
                    products.offer_type = None
                    products.offer_name = None          
                    products.offer_percent = None        
                    products.expiry_date = None      
                    products.expiry_time = None
                    products.save()
                    return redirect('add_product_offer')

    elif request.method == 'GET':
        return render(request,'add_product_offer.html',context)

def add_coupon(request):
    if request.method == 'POST':
        coupon_name      = request.POST['coupon_name'].upper()
        coupon_percent   = request.POST['coupon_percent']
        expiry_date     = request.POST['expiry_date']
        expiry_time     = request.POST['expiry_time']
        coupon = Coupon.objects.create(coupon_name=coupon_name,coupon_percent=coupon_percent,expiry_date=expiry_date,expiry_time=expiry_time)
    else:
        return render(request,'add_coupon.html')
    return render(request,'add_coupon.html') 

def view_coupon(request):
    coupons = Coupon.objects.all()
    return render(request,'view_coupon.html',{'coupons':coupons})

def apply_coupon(request,total=0,tax=0,grand_total=0,quantity=0,cart_items=None):
    address = Address.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        get_coupon = request.POST.get('coupon').upper()
        get_coupon
        print("get coupon",get_coupon)
        coupon = Coupon.objects.get(coupon_name=get_coupon)
        print("coupon percent",coupon.coupon_percent)
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        if coupon:
            print("coupon case")
            for cart_item in cart_items:
                total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
                print("total",total)
                quantity += cart_item.quantity
                tax = (2 * total)/100
                grand_total = total + tax
                print('grand total',grand_total)
                grand_total = grand_total-(grand_total/coupon.coupon_percent)
                messages.info(request, 'Your coupon has been applied!')
                
        else:
            print('else caseeeeeeeeeee')
            for cart_item in cart_items:
                total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
                quantity += cart_item.quantity
                tax = (2 * total)/100
                grand_total = total + tax

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax' : tax,
            'grand_total' : grand_total,
            'address':address
        }
        return render(request, 'checkout.html',context)
    else:
        return render(request, 'checkout.html')
    
  