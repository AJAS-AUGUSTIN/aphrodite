from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Account
from category.models import Address
from category.models import Products
from category.views import address
from orders.models import OrderItems, OrderProduct,Order
from .models import Cart, CartItem, CartItems
from django.contrib.auth.decorators import login_required
import json
import datetime
import uuid

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        return cart


def add_cart(request, id):
    product = Products.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=request.user.username)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = request.user.username
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, id):
    cart = Cart.objects.get(cart_id=request.user.username)
    product = get_object_or_404(Products,id = id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, id):
    cart = Cart.objects.get(cart_id = request.user.username)
    product = get_object_or_404(Products,id = id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,tax=0,grand_total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
            user_id = request.user.id
            OrderProduct.objects.create(quantity=quantity,grand_total=grand_total,tax=tax,user_id=user_id)
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
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
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
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

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
        print(user_id)
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
        print('hi')
        address = Address.objects.create(user_id=users,first_name=first_name, last_name=last_name,email=email,phone_number=phone_number,address_line_1=address_line_1,address_line_2=address_line_2,city=city,state=state,country=country,order_note=order_note,pincode=pincode)
    return render(request,'final.html')

def place_order(request):
    current_user = request.user
    if request.method == 'POST':
        address_data = Address.objects.get(user_id = current_user)
        payment_method  = payment = request.POST['cash']
         
        # creating order number using uuid
        order_id = str(uuid.uuid4())
        user_id = current_user.id
        status = "ordered"
        
        order = Order.objects.create(order_id = order_id, payment_mode = payment_method, user =  current_user, user_address = address_data,status=status )
        cart_items = CartItem.objects.filter(user=current_user)
        for items in cart_items:
            single_order = order
            print(single_order)
            user = current_user
            print(user)
            product_id = items.products_id
            print(product_id)
            quantity = items.quantity 
            print(quantity)
            sub_total = items.sub_total
            print(sub_total)
            is_active = items.is_active
            print(is_active)

            cart_orders = OrderItems.objects.create(order = single_order, user = user, products_id = product_id, quantity = quantity, sub_total = sub_total, is_active = is_active)
            if payment_method == 'cash_on_delivery':
                CartItems.objects.filter(user = current_user).delete()

    return render(request,'final.html')


    cart_items = CartItem.objects.filter(user=current_user)
    orderproduct = OrderProduct.objects.filter(user=current_user)
    grand_total = orderproduct.grand_total

    tax = orderproduct.tax
    user_id = current_user.id
    if request.method == 'POST':
        
    else:
        pass
    Orders.objects.create(payment_mode = payment,user_address = address_data,order_total=grand_total,tax=tax,user_id=user_id)
    cart_items.delete()
    return render(request,'final.html')


# def place_order(request):
#     current_user = request.user
#     address_data = Address.objects.filter(user_id = current_user)
#     user_data=Account.objects.get(username=request.user)
#     address_id = request.POST.get('address')
#     payment = request.POST.get('payment_method')
#     date = datetime.datetime.now()
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     sub_total = 0

#     for each_product in cart_items:
#                 product_id=each_product.products_id.id
#                 quantity = each_product.quantity
#                 total = each_product.total
#                 product=Products.objects.get(id=product_id)
#                 product.unit-=quantity
#                 sub_total += total

#     order = Orders.objects.create(user=current_user,user_address=address_data,payment=payment,status="ordered")
#     cart_items.delete()

#     if cart_count <= 0:
#         return redirect('home')
#     else:
#         return render(request, 'final.html',{'address_data':address_data})
         
# def payments(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])

#     #store transactions details inside payment model

#     payment = Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = order.order_total,
#         status = body['status']
#     )
#     payment.save()

#     order.payment = payment
#     order.is_ordered = True
#     order.save()

#     #move the cart items to order product table
#     cart_items = CartItem.objects.filter(user=request.user)

#     for item in cart_items:
#         orderproduct = OrderProduct()
#         orderproduct.order_id = order.id
#         orderproduct.payment = payment
#         orderproduct.user_id = request.user.id
#         orderproduct.product_id = item.product_id
#         orderproduct.quantity = item.quantity
#         orderproduct.quantity = item.quantity
#         orderproduct.product_price = item.product.price
#         orderproduct.ordered = True
#         orderproduct.save()