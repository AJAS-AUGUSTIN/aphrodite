from django.db.models import base
from django.shortcuts import render
from category.models import Categories, Products
from carts.models import CartItems , Wishlist
from carts.views import _cart_id
from store.models import Banner

def home(request):
    product = Products.objects.all().filter(is_available=True)
    categories = Categories.objects.all()
    user = request.user.id
    cartitems = CartItems.objects.filter(user=user)
    banners = Banner.objects.all()
    for pro in product:
        products = Products.objects.filter(id=pro.id).first()
    
    context = {
        'product':product,
        'categories':categories,
        'cartitems':cartitems,
        'banners':banners
    }
    return render(request, 'home.html',context)