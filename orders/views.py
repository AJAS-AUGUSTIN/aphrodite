from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from carts.models import CartItem
from category.models import Address
from orders.models import Orders
# from .forms import OrderForm
import datetime

# Create your views here.

def orders(request):
    return render(request, 'orders.html')

