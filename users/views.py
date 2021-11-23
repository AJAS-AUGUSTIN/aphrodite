from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User, auth
from accounts.models import Account
from django.contrib import messages
# from .twilio import send_sms, verify
from twilio.rest import Client
from carts.models import Cart, CartItem
from category.models import Order, OrderItem, Products
from django.http import JsonResponse
import json
from carts.views import _cart_id
import requests

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
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

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
                auth_token = '9cc56d0c79c60ce2ffa31d1ba8070990'
                client = Client(account_sid, auth_token)

                verification = client.verify \
                    .services('VA6079c3a298552f5faf28187878be1048') \
                    .verifications \
                    .create(to=phone_number, channel='sms')
                print('entry')
                return render(request, 'otpentry.html', {'phone_number': phone_number})
            else:
                messages.info(request, 'The phone number does not exist',
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
            auth_token = '9cc56d0c79c60ce2ffa31d1ba8070990'
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

def productdetails(request,id):
    print(id)
    products = Products.objects.filter(id=id)
    return render(request, 'productdetails.html',{'products':products})

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
