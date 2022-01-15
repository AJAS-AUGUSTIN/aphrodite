import re
from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.models import User, auth
from accounts.models import Account
from django.contrib import messages
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
from django.conf import settings


# Create your views here.
@never_cache
def login(request):
    if request.session.has_key('username'):
        return render(request, 'home.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        request.session['username'] = True
        auth.login(request, user)
        if user is not None:
            # cart functionality
            try:
                cart = request.session['guest_cart']
                is_cart_item_exists=CartItems.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItems.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.cart = None
                        item.save()
                        del request.session['guest_cart']
            except:
                pass
            #cart functionality ends
            
            url = request.META.get('HTTP_REFERER')
            try:
                query = request.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if next in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect(home)
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect(login)
    else:
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
                messages.info(request, 'Username Taken')
                return redirect(register)
            elif Account.objects.filter(email=email).exists():
                messages.info(request, 'E-mail Taken')
                return redirect(register)
            else:
                user = Account.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('register')
    else:
        return render(request, 'registration.html')


def home(request):
    product = Products.objects.all()
    return render(request, 'home.html',{'product':product})


def otp(request):
    return render(request, 'otp.html')


def login_with_otp(request):
    if request.session.has_key('phone'):
        return redirect(home)
    else:
        if request.method == 'POST':
            phone_number = request.POST['phone_number']
            if Account.objects.filter(phone_number=phone_number).exists():
                phone_number = '+91'+str(phone_number)
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services(settings.TWILIO_SERVICE_ID) \
                    .verifications \
                    .create(to=phone_number, channel='sms')
                return render(request, 'otpentry.html', {'phone_number': phone_number})
            else:
                messages.info(request, "The phone number does not exist",
                              extra_tags="phone_number_otp_error")
                return render(request, 'otp.html')
        else:
            return render(request, 'otp.html')


def check_otp(request,phone_number):
    if request.session.has_key('phone'):
        return redirect(home)
    else:
        if request.POST.get('otp') != None:
            user_phone_number = phone_number[3:]
            user = Account.objects.get(phone_number=user_phone_number)
            otp_user = request.POST['otp']
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            verification_check = client.verify \
                .services(settings.TWILIO_SERVICE_ID) \
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
    try:
        products = Products.objects.filter(id=id).first()
        if request.user.is_authenticated:
            in_cart = CartItems.objects.filter(user=request.user,product=products).exists()
        else:
            cart = request.session['guest_cart']
            in_cart = CartItems.objects.filter(cart=cart,product=products).exists()
    except:
        in_cart=0
        pass
    
    context = {
        'product':products,
        'in_cart':in_cart,
    }
    return render(request, 'productdetails.html',context)

def userdetails(request):
    if request.session.has_key('username'):
        user = Account.objects.get(id = request.user.id)
        order_item = OrderItems.objects.filter(user = user).order_by('-id')
        order = Order.objects.filter(user = user)
        product = Products.objects.filter(id=user.id)
        context = {
            'order_item':order_item,
            'product':product,
        }
        return render(request,'userdetails.html', context)
    elif request.session.has_key('phone'):
        user = Account.objects.get(id = request.user.id)
        order_item = OrderItems.objects.filter(user = user).order_by('-id')
        order = Order.objects.filter(user = user)
        product = Products.objects.filter(id=user.id)
        context = {
            'order_item':order_item,
            'product':product,
        }
        return render(request,'userdetails.html', context)
    else:
        return redirect('login')

def cancel_order_user(request, id):
    user = Account.objects.get(id = request.user.id)
    order = OrderItems.objects.get(id = id)
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
