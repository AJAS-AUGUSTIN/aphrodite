from django.shortcuts import render
from category.models import Categories, Products

def home(request):
    product = Products.objects.all().filter(is_available=True)
    categories = Categories.objects.all()
    for pro in product:
        if pro.offer_name != None:
            pro.product_discount_price =  pro.product_discount_price-(pro.product_discount_price/pro.offer_percent)
        else:
            pass
    return render(request, 'home.html',{'product':product},{'categories':categories})