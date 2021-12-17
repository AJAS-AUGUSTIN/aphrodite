from django.shortcuts import render
from category.models import Categories, Products
from carts.models import CartItems

def home(request):
    product = Products.objects.all().filter(is_available=True)
    categories = Categories.objects.all()
    user = request.user.id
    cartitems = CartItems.objects.filter(user=user)
    context = {
        'product':product,
        'categories':categories,
        'cartitems':cartitems
    }
    return render(request, 'home.html',context)