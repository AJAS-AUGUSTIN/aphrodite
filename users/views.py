import re
from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.models import User, auth
from accounts.models import Account
from django.contrib import messages
# from .twilio import send_sms, verify
from twilio.rest import Client
from carts.models import Cart, CartItems
from category.models import Address, Products
from django.http import JsonResponse
import json
from carts.views import _cart_id
import requests
from orders.models import Order, OrderItems
from orders.views import orders
from django.contrib.auth import update_session_auth_hash

# Create your views here.


@never_cache
def login(request):
    if request.session.has_key('username'):
        return render(request, 'home.html')
    elif request.method == 'POST':
        print('index POST req received')
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_superadmin == False:
            # cart functionality
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_item=request.user.username)
                    is_cart_item_exists=CartItems.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItems.objects.filter(cart=cart)

                        for item in cart_item:
                            item.user = user
                            item.save()
                except:
                    pass
            #cart functionality ends
            request.session['username'] = True
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = request.utils.urlparse(url).query
                print('query=',query)
                params = dict(x.split('=') for x in query.split('&'))
                print('params=',params)
                if next in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect(home)
        else:
            print('else case')
            print('username and password not verified')
            messages.info(request, 'Invalid Credentials')
            return redirect(login)
    else:
        print('index GET req received')
    return render(request, 'login.html')


def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
    elif request.session.has_key('phone'):
        del request.session['phone']
    auth.logout(request)
    return redirect(home)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']

        if password1 == password2:
            if Account.objects.filter(username=username).exists():
                print("username taken")
                messages.info(request, 'Username Taken')
                return redirect(register)
            elif Account.objects.filter(email=email).exists():
                print("email taken")
                messages.info(request, 'E-mail Taken')
                return redirect(register)
            else:
                user = Account.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
                user.save()
                print("usercreated")
                return redirect('login')

        else:
            print("Password not matching")
            messages.info(request, 'Passwords Not Matching')
            return redirect('register')
        # return redirect('/')
    else:
        return render(request, 'registration.html')


def home(request):
    print("enterd")
    product = Products.objects.all()
    print(product)
    return render(request, 'home.html',{'product':product})


def otp(request):
    return render(request, 'otp.html')


# def login_with_otp(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         if Account.objects.filter(phone_number=phone_number).exists():
#             user = Account.objects.filter(phone_number=phone_number)
#             if user:
#                 sid=send_sms(phone_number)
#                 request.session['phone']=phone_number
#                 request.session['sid']=sid
#                 return render(request, 'otpentry.html')
#             else:
#                 print('not logged in with otp')
#                 messages.info(request, 'invalid phone number')
#                 return redirect('otp')
#         return redirect('otp')

def login_with_otp(request):
    if request.session.has_key('phone'):
        print('direct entry')
        return redirect(home)
    else:
        if request.method == 'POST':
            phone_number = request.POST['phone_number']
            if Account.objects.filter(phone_number=phone_number).exists():
                phone_number = '+91'+str(phone_number)
                account_sid = 'AC8d1ed90c743abe70963aa42514c5587d'
                auth_token = 'a8b1081205e9991a3a07bd8f22f933f6'
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services('VA6079c3a298552f5faf28187878be1048') \
                    .verifications \
                    .create(to=phone_number, channel='sms')
                print('entry')
                return render(request, 'otpentry.html', {'phone_number': phone_number})
            else:
                messages.info(request, "The phone number does not exist",
                              extra_tags="phone_number_otp_error")
                print('phone number error')
                return render(request, 'otp.html')
        else:
            print('else case')
            return render(request, 'otp.html')

def check_otp(request,phone_number):
    if request.session.has_key('phone'):
        return redirect(home)
    else:
        if request.POST.get('otp') != None:
            user_phone_number = phone_number[3:]
            user = Account.objects.get(phone_number=user_phone_number)
            otp_user = request.POST['otp']
            account_sid = 'AC8d1ed90c743abe70963aa42514c5587d'
            auth_token = '8598d7e084fb986c574238d3fd992334'
            client = Client(account_sid, auth_token)
            verification_check = client.verify \
                .services('VA6079c3a298552f5faf28187878be1048') \
                .verification_checks \
                .create(to=phone_number, code=otp_user)
            if verification_check.status == "approved":
                request.session['phone'] = True
                auth.login(request, user)
                return redirect(home)
            else:
                messages.info(request, 'Invalid Otp')
                return render(request, 'otpentry.html')
        else:
            return render(request, 'otpentry.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productdetails(request,id):
    products = Products.objects.filter(id=id)
    # in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request),product=products).exists()
    # print(in_cart)
    for pro in products:
        if pro.offer_name != None:
            pro.product_discount_price =  pro.product_discount_price-(pro.product_discount_price/pro.offer_percent)
        else:
            pass
    # try:
    #     in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request),product=products).exists()
    #     return HttpResponse(in_cart)
    #     exit()  
    # except:
    #     print('except')
    #     pass

    return render(request, 'productdetails.html',{'products':products})

def userdetails(request):
    if request.session.has_key('username'):
        user = Account.objects.get(id = request.user.id)
        order_item = OrderItems.objects.filter(user = user)
        order = Order.objects.filter(user = user)
        product = Products.objects.filter(id=user.id)
        context = {
            'order':order,
            'order_item':order_item,
            'product':product,
        }
        return render(request,'userdetails.html', context)
    else:
        return redirect('login')

def cancel_order_user(request, id):
    user = Account.objects.get(id = request.user.id)
    print(user)
    order = Order.objects.get(id = id)
    print(order)
    order.delivery_status = 'cancelled'
    order.save()
    return redirect('userdetails')

def editaddress(request,id):
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.email = request.POST['email']
        address.phone_number = request.POST['phone_number']
        address.address_line_1 = request.POST['address_line_1']
        address.address_line_2 = request.POST['address_line_2']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.pincode = request.POST['pincode']
        address.order_note = request.POST['order_note']
        address.save()
        return redirect('listaddress')

    else:
        return render(request,'addresschange.html', {'address' : address})

def editaddress_checkout(request,id):
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.email = request.POST['email']
        address.phone_number = request.POST['phone_number']
        address.address_line_1 = request.POST['address_line_1']
        address.address_line_2 = request.POST['address_line_2']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.pincode = request.POST['pincode']
        address.order_note = request.POST['order_note']
        address.save()
        return redirect('checkout')

    else:
        return render(request,'editaddress_checkout.html', {'address' : address})

def listaddress(request):
    address = Address.objects.filter(user_id=request.user.id)
    print(address)
    return render(request,'listaddress.html',{'address': address})

def deleteaddress(request,id):
    address = Address.objects.filter(id=id)
    try:
        address.delete()
        return redirect('listaddress')
    except:
        pass

def add_address_checkout(request):
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
        return redirect('checkout')
    else:
        return render(request,'add_address_checkout.html')

def change_password(request):
    if request.method == 'GET':
        return render(request,'change_password_user.html')
    else:
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if current_password and new_password and new_password == confirm_password:
            current_user = Account.objects.get(id=request.user.id)
            
            if current_user.check_password(current_password):
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash (
                    request,
                    current_user
                )
                messages.info(request,"Password Sucessfully changed")
                return redirect('userdetails')
            else:
                messages.info(request,"old password incorrect")
                return redirect('change_password')
        else:
            messages.info(request,"Invalid")
            return redirect('change_password')

def account_details(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.save()
        return redirect('userdetails')
    else:
        return render(request,'account_details.html',{'user':user})





#---------------dennisivy starts-----------------

# def cart(request,id):
#     if request.user.is_authenticated:
#         # first_name = Account.objects.filter(first_name=first_name)
#         first_name = request.user.first_name
#         order, created = Order.objects.get_or_create(customer=first_name, complete=False)
#     products = Products.objects.filter(id=id)
#     return render(request, 'cart.html',{'products':products})

# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     print('Action:',action)
#     print('productId:',productId)

#     first_name = request.user.first_name
#     product = Products.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=first_name, complete=False)
#     orderItem, created = OrderItem.objects.get_or_create(order = order, product=product)

#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
    
#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()

#     return JsonResponse('item was added', safe=False)


#-----------------dennisivy ends-----------



# def check_otp(request):
#     if request.method == 'POST':
#         otp_num = request.POST.get('otp')
#         if request.session.has_key('logged_in'):
#             return render(request, 'home.html')
#         else:
#             mobile_num=request.session['phone']
#             sid=request.session['sid']
#             checker=verify(otp_num,mobile_num,sid)
#             print(checker)
#             user = Account.objects.filter(phone_number=mobile_num)
#             if checker == 'approved':
#                 request.session['logged_in'] = True
#                 auth.login(request, user)
#                 return redirect(home)
#             else:
#                 print('hello')
#                 messages.error(request, "invalid otp")
#                 return redirect('')
#     else:
#         return redirect('login')
