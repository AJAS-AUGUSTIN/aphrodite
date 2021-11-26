from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from category.models import Address
# from .forms import OrderForm
import datetime

from orders.models import Order

# Create your views here.

def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html',{'orders':orders})

def editordersadmin(request,id):
    order = Order.objects.get(id=id)
    return render(request,'editordersadmin.html',{'order':order})

def statuschange(request,id):
    status = request.POST['status']
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delivery_status = status
        order.save()
        return redirect('orders')
    else:
        pass

