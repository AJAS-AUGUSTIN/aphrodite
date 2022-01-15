from django.contrib.messages.api import success
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache , cache_control
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from accounts.models import Account
import carts
from category.models import Address, Coupon
from category.models import Products
from django.http import JsonResponse
# from category.views import address
from orders.models import OrderItems,Order, Payment
from .models import Cart, CartItems, WishCart, Wishlist
from django.contrib.auth.decorators import login_required
import json
import datetime
import uuid
import razorpay
from django.contrib import messages

from django.conf import settings

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session['session'] = str(uuid.uuid4())
        cart = request.session['session']
        return cart
    else:
        return cart


@csrf_exempt
def add_cart(request):
    current_user = request.user
    if request.method == 'POST':
        product_id = request.POST['id']
        product = Products.objects.get(id=product_id)
        # if the user is authenticated
        if current_user.is_authenticated:
            try:
                cart_item = CartItems.objects.get(product=product,user=request.user)
                if cart_item.quantity < 10:
                    count = cart_item.product.stock
                    if cart_item.quantity < count:
                        cart_item.quantity += 1
                        cart_item.save()
                    else:
                        return JsonResponse({'error':"No stocks"})
                    return JsonResponse({'alert':"Item already in Cart!! Added the quantity"})  
                else:
                    return JsonResponse({'max':"Item already in Cart!! Maximum limit reached"})
            except CartItems.DoesNotExist:
                cart_item = CartItems.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user,
                )
                cart_item.save()
            success = "Item added to cart"
            cart_items_count = CartItems.objects.filter(user = request.user).count()
            return JsonResponse({'success':success,'cart_count':cart_items_count})

        # if user is not authenticated
        else:
            try:
                cart = request.session['guest_cart']
            except:
                cart = request.session['guest_cart'] = str(uuid.uuid4())

            is_cart_item_exists = CartItems.objects.filter(product=product,cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItems.objects.filter(product=product,cart=cart)

            try:
                cart_item = CartItems.objects.get(product=product,cart=cart)
                if cart_item.quantity < 10:
                    count = cart_item.product.stock
                    if cart_item.quantity < count:
                        cart_item.quantity += 1
                        cart_item.save()
                    else:
                        return JsonResponse({'error':"No stocks"})
                    return JsonResponse({'alert':"Item already in Cart!! Added the quantity"})  
                else:
                    return JsonResponse({'max':"Item already in Cart!! Maximum limit reached"})
            except CartItems.DoesNotExist:
                cart_item = CartItems.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                    user_id=request.user.id,
                )
                cart_item.save()
                cart_items_count = CartItems.objects.filter(user = None,cart=cart).count()
                return JsonResponse({'success':"Item added to cart",'cart_count':cart_items_count})


def cart_inc(request,id):
    product = get_object_or_404(Products,id = id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(product=product,user=request.user)
    else:
        cart_item = CartItems.objects.get(cart=request.session['guest_cart'],product=product)
    if cart_item.quantity < 10:
        count = cart_item.product.stock
        if cart_item.quantity < count:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.info(request, 'No stocks')
    else:
        messages.info(request, 'Maximum limit reached')
    return redirect('cart')


def remove_cart(request, id):
    product = get_object_or_404(Products,id = id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(product=product,user=request.user)
    else:
        cart_item = CartItems.objects.get(cart=request.session['guest_cart'],product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.error(request,'Quantity cannot be decreased.Please use Remove button to remove from cart')
    return redirect('cart')


@csrf_exempt
def remove_cart_item(request):
    id = request.POST.get('cart_item')
    product = get_object_or_404(Products,id = id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(product=product,user=request.user)
    else:
        cart_item = CartItems.objects.get(cart=request.session['guest_cart'],product=product)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,tax=0,grand_total=0, quantity=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        else:
            if request.session.has_key('guest_cart'):
                cart = request.session['guest_cart']
                cart_items = CartItems.objects.filter(cart=cart, is_active=True)
            else:
                cart_items = []
        
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
            user_id = request.user.id
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def checkout(request,total=0,tax=0,grand_total=0,quantity=0,cart_items=None):
    address = Address.objects.filter(user_id=request.user.id)
    try:
        cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        get_coupon = request.POST.get('coupon')
        coupon = Coupon.objects.filter(coupon_name=get_coupon)
        if coupon:
            for cart_item in cart_items:
                total += ((int(cart_item.product.product_discount_price) * int(cart_item.quantity))/coupon.coupon_percent)
                quantity += cart_item.quantity
                tax = (2 * total)/100
                grand_total = total + tax
        else:
            for cart_item in cart_items:
                total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
                quantity += cart_item.quantity
                tax = (2 * total)/100
                grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'address' : address
    }
    return render(request, 'checkout.html',context)

def final(request):
    total=0
    quantity=0
    try:
        cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
    
    if request.method == 'POST':
        user_id = request.user.id
        users=Account.objects.get(id=user_id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        order_note = request.POST['order_note']
        pincode = request.POST['pincode']
        address = Address.objects.create(user_id=users,first_name=first_name, last_name=last_name,email=email,phone_number=phone_number,address_line_1=address_line_1,address_line_2=address_line_2,city=city,state=state,country=country,order_note=order_note,pincode=pincode)
    return render(request,'final.html')

def place_order(request):
    current_user = request.user

    if request.method == 'POST':
        address = request.POST['address']
        address_data = Address.objects.get(id=address)
        if request.POST.get('payment_method') == 'cash_on_delivery':
            payment_method  = request.POST['payment_method']
            payment_status = "Pending"
        elif request.POST.get('payment_method') == 'razor_pay':
            payment_method  = request.POST['payment_method'] 
            payment_status = "COMPLETED"
        else:
            payment_method  = request.POST['payment_method'] 
            payment_status = "pending"        
        #taking payment id generated by razor pay
        if request.POST.get('payment_id'):
            payment_id = request.POST['payment_id']
        else:
            payment_id = 0
        # creating order number using uuid
        order_id = str(uuid.uuid4())
        order_status = "ordered"
        user = request.user.id
        ordered_user = Account.objects.get(id = user)
        # taking the address
        ordered_address = address_data.first_name + ", \n" + \
            address_data.address_line_1 + "\n" + \
            address_data.state + ", " + str(address_data.pincode) + "\n" + \
            address_data.country + " ,\n" + \
            address_data.phone_number 
        # order is instance of particular order 
        grand_total = request.POST.get('hidden_grand_total')
        order = Order.objects.create(order_id = order_id, payment_method = payment_method, user =  ordered_user, delivered_address = ordered_address, delivery_status = order_status,grand_total=grand_total,payment_status=payment_status )
        cart_items = CartItems.objects.filter(user = ordered_user)
        total=0
        quantity=0
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
        for items in cart_items:
            single_order = order
            user = ordered_user
            product_id = items.product_id
            product = Products.objects.get(id = product_id)
            quantity = items.quantity 
            sub_total = items.sub_total
            is_active = items.is_active
            grand_total = grand_total
            sub=items.sub_total()
            cart_orders = OrderItems.objects.create(order = single_order, user = user, products_id = product, quantity = quantity,delivery_status = order_status,is_active = is_active,sub_total = sub,grand_total=grand_total)
            Payment.objects.create(user = current_user, payment_id = payment_id, payment_method = payment_method, amount_paid = grand_total, status = payment_status, order = order  )
            #deleting cart items
            CartItems.objects.filter(user = ordered_user).delete()
            product.stock -= items.quantity
            product.save()
            context = {
                    'product_name':product.product_name,
                    'product_brand':product.brand,
                    'order_address': ordered_address,
                    'payment_method': payment_method,
                    'order_status': order_status,
                    'grand_total':grand_total

            }
            return render(request, 'final.html', context)

    return render(request, 'final.html')


# paypal payment
@csrf_exempt
def paypal_payment(request):
    body = json.loads(request.body)
    transaction_id = body['transID']
    grand_total_hidden = request.POST.get('hidden_grand_total')
    id = request.user.id
    current_user = Account.objects.get(id = id)
    address_id = body['address_id']
    address_data = Address.objects.get(id = address_id) 
    delivery_status = 'ordered'
    ordered_address = address_data.first_name + ", \n" + \
            address_data.address_line_1 + "\n" + \
            address_data.state + ", " + str(address_data.pincode) + "\n" + \
            address_data.country + " ,\n" + \
            address_data.phone_number
    new_order = Order.objects.create(user = current_user,order_id  = body['orderID'], payment_method = body['payment_methods'], delivered_address = ordered_address, delivery_status = delivery_status, payment_status = body['status'], grand_total = body['grand_total'] )
    Payment.objects.create(user = current_user, payment_id = body['transID'], payment_method = body['payment_methods'], amount_paid = body['grand_total'], status = body['status'], order = new_order  )
    #moving the cart products to order items 
    cart_items = CartItems.objects.filter(user = current_user)
    total=0
    quantity=0
    for cart_item in cart_items:
        total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
        quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        grand_total = grand_total
        sub=cart_item.sub_total()
        OrderItems.objects.create(quantity = cart_item.quantity,grand_total=grand_total,delivery_status = delivery_status, products_id = cart_item.product, sub_total = sub, user = current_user, order = new_order)
        #reducing the product stock
        product = Products.objects.get(id = cart_item.product.id)
        product.stock -= cart_item.quantity
        product.save()
    cart_items.delete()
    # Taking new order id
    new_order_id = new_order.id
    data = {
        'new_order_id' :new_order_id ,
        'transID' : transaction_id,
    }
    return JsonResponse(data, safe=False)
    
# paypal success
    
@csrf_exempt
@never_cache
def paypal_payment_success(request):
    order_id = request.GET.get('order_id')
    trans_id = request.GET.get('trans_id')
    cart_items = CartItems.objects.filter(user = request.user)
    current_order = Order.objects.get(id = order_id)
    order_id= current_order.order_id,
    order_address= ''.join(current_order.delivered_address),
    payment_method= current_order.payment_method,
    order_status= current_order.delivery_status,
    grand_total=current_order.grand_total
    for cart_item in cart_items:
        product = Products.objects.get(id = cart_item.product.id)
        context = {
        'product_name':product.product_name,
        'product_brand':product.brand,
        'order_address': order_address,
        'payment_method': payment_method,
        'order_status': order_status,
        'grand_total':grand_total

        }
        return render(request, 'user/order_details.html', context)
    context = {
        'order_address': order_address,
        'payment_method': payment_method,
        'order_status': order_status,
        'grand_total':grand_total

        }
    return render(request, 'user/order_details.html',context)


def payment_error(request):
    return render(request, 'payment_error.html' )


# razorpay payment
@csrf_exempt
@never_cache
def razor_pay_details(request):
    grand_total = float(request.POST.get('total_amount'))
    amount = grand_total*100
    currency = "INR"
    data = { 
        "amount": amount, 
        "currency": currency, 
        "receipt": "order_rcptid_11" 
        }
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    razor_pay_order = razorpay_client.order.create(data=data)
    razor_pay_order_id = razor_pay_order['id']
    context = {
        'grand_total' : amount,
        'razor_pay_order_id' : razor_pay_order_id,
        'currency' : currency,
    }
    return JsonResponse(context, safe=False)


@login_required(login_url='login')
def buy_now(request,id,total=0,tax=0,grand_total=0,quantity=0,cart_items=None):
    address = Address.objects.filter(user_id=request.user.id)
    product = Products.objects.get(id=id)
    try:
        cart_item = CartItems.objects.get(product=product,user=request.user)
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(
            product = product,
            quantity = 1,
            user_id=request.user.id,
        )
        cart_item.save()
    try:
        cart_items = CartItems.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'address' : address
    }
    return render(request, 'checkout.html',context)


def _wishcart_id(request):
    wishcart = request.session.session_key
    if not wishcart:
        request.session['wishsession'] = str(uuid.uuid4())
        wishcart = request.session['wishsession']
        return wishcart
    else:
        return wishcart 

def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user = request.user)
        context = {
            'wishlist_items': wishlist_items,
        }
        return render (request, 'wishlist.html',context)
    else:
        return render (request, 'wishlist.html')

@csrf_exempt
def add_wishlist(request):    
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user = request.user.id)
        if request.method == 'POST':
            if request.user.is_authenticated:                
                product_id = request.POST['id']
                user = Account.objects.get(id = request.user.id)
                product = Products.objects.get(id = product_id)            
                wishlist = Wishlist()
                wishlist.product = product
                wishlist.user = user
                wish_item = Wishlist.objects.filter(product = product, user = request.user).first()
                if wish_item:
                    wish_item_count = Wishlist.objects.filter(user = request.user).count()
                    alert = 'Already added!!!'
                    return JsonResponse({'alert': alert,'wish_items':wish_item_count})                  
                else:                    
                    wishlist.save()
                wish_item_count = Wishlist.objects.filter(user = request.user).count()
                success = 'product added to wishlist!!!'
                return JsonResponse({'success': success,'wish_items':wish_item_count})
            else:
                try:
                    wishcart = WishCart.objects.get(wishcart_id=_wishcart_id(request))
                except WishCart.DoesNotExist:
                    wishcart = WishCart.objects.create(
                    wishcart_id = _wishcart_id(request)
                    )
                    cart.save()
                error = "error"
                return JsonResponse({'error':error })
    else:
        messages.error(request,"please login!!")
        return redirect('login')
    wishlist_items = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render (request, 'wishlist.html',context)


def remove_wish_item(request):
    product_id =request.GET['prodId']
    wishlist_item = Wishlist.objects.get(product = product_id)
    wishlist_item.delete()
    return JsonResponse({'success':'Item successfully Removed'})



