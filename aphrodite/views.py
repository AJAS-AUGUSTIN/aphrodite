from django.shortcuts import render
from category.models import Categories, Products

def home(request):
    product = Products.objects.all().filter(is_available=True)
    categories = Categories.objects.all()
    return render(request, 'home.html',{'product':product},{'categories':categories})