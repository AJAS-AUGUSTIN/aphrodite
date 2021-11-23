from django.shortcuts import render
from category.models import Categories, Products

def home(request):
    product = Products.objects.all()
    categories = Categories.objects.all()
    return render(request, 'home.html',{'product':product},{'categories':categories})