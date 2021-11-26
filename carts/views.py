from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache , cache_control
from accounts.models import Account
from category.models import Address
from category.models import Products
# from category.views import address
from orders.models import OrderItems,Order
from .models import Cart, CartItems
from django.contrib.auth.decorators import login_required
import json
import datetime
import uuid

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        return cart

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
        cart_item = CartItems.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            user_id=request.user.id,
            # sub_total = CartItems.sub_total(),
        )
        cart_item.save()
    return redirect('cart')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_cart(request, id):
    cart = Cart.objects.get(cart_id=request.user.username)
    product = get_object_or_404(Products,id = id)
    cart_item = CartItems.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_cart_item(request, id):
    cart = Cart.objects.get(cart_id = request.user.username)
    product = get_object_or_404(Products,id = id)
    cart_item = CartItems.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request,total=0,tax=0,grand_total=0, quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        # products = get_object_or_404(Products,id = id)
        # product=Products.objects.get(product=products)
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
            # sub_total = product.product_discount_price * quantity
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
        cart = Cart.objects.get(cart_id=request.user.username)
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
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
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)

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
        payment_method = request.POST['cash']
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

        print(ordered_address)

        # order is instance of particular order
        
        order = Order.objects.create(order_id = order_id, payment_method = payment_method, user =  ordered_user, delivered_address = ordered_address, delivery_status = order_status )

        print(order.order_id)

        cart_items = CartItems.objects.filter(user = ordered_user)
        total=0
        quantity=0
        for cart_item in cart_items:
            total += (int(cart_item.product.product_discount_price) * int(cart_item.quantity))
            quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
            print(grand_total)

        for items in cart_items:
            single_order = order
            user = ordered_user
            product_id = items.product_id
            product = Products.objects.get(id = product_id)
            print(product_id)
            quantity = items.quantity 
            sub_total = items.sub_total
            is_active = items.is_active
            grand_total = grand_total

            cart_orders = OrderItems.objects.create(order = single_order, user = user, products_id = product, quantity = quantity,is_active = is_active,grand_total=grand_total)

            

        if payment_method == 'cash on delivery':
            CartItems.objects.filter(user = ordered_user).delete()

            context = {
                    'order_id': order_id,
                    'order_address': ordered_address,
                    'payment_method': payment_method,
                    'order_status': order_status

            }


            return render(request, 'final.html', context)

        # else:
        #     return redirect('home')

# deleting cart item

# @csrf_exempt
# def delete_product(request):
#     item_id = request.POST['item_id']
#     CartItems.objects.get(id = item_id).delete()
#     return JsonResponse('',safe=False)
    # cart_items = CartItems.objects.filter(user=current_user)
    # OrderItems = OrderItems.objects.filter(user=current_user)
    # grand_total = OrderItems.grand_total

    # tax = OrderItems.tax
    # user_id = current_user.id
    # if request.method == 'POST':
    #     pass
    # else:
    #     pass
    # Orders.objects.create(payment_mode = payment,address_data = address_data,order_total=grand_total,tax=tax,user_id=user_id)
    # cart_items.delete()
    # return render(request,'final.html')


# def place_order(request):
#     current_user = request.user
#     address_data = Address.objects.filter(user_id = current_user)
#     user_data=Account.objects.get(username=request.user)
#     address_id = request.POST.get('address')
#     payment = request.POST.get('payment_method')
#     date = datetime.datetime.now()
#     cart_items = CartItems.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     sub_total = 0

#     for each_product in cart_items:
#                 product_id=each_product.products_id.id
#                 quantity = each_product.quantity
#                 total = each_product.total
#                 product=Products.objects.get(id=product_id)
#                 product.unit-=quantity
#                 sub_total += total

#     order = Orders.objects.create(user=current_user,address_data=address_data,payment=payment,status="ordered")
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
#     cart_items = CartItems.objects.filter(user=request.user)

#     for item in cart_items:
#         OrderItems = OrderItems()
#         OrderItems.order_id = order.id
#         OrderItems.payment = payment
#         OrderItems.user_id = request.user.id
#         OrderItems.product_id = item.product_id
#         OrderItems.quantity = item.quantity
#         OrderItems.quantity = item.quantity
#         OrderItems.product_price = item.product.price
#         OrderItems.ordered = True
#         OrderItems.save()