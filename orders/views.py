import re
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from category.models import Address
# from .forms import OrderForm
import datetime
from orders.models import Order, OrderItems


# Create your views here.
def orders(request):
    orders = OrderItems.objects.all().order_by('-id')
    return render(request, 'orders.html',{'orders':orders})


def editordersadmin(request,id):
    order = Order.objects.get(id=id)
    return render(request,'editordersadmin.html',{'order':order})


def statuschange(request,id):
    status = request.POST['status']
    order = OrderItems.objects.get(id=id)
    if request.method == 'POST':
        order.delivery_status = status
        order.save()
        return redirect('orders')
    else:
        pass


def sales_report(request):
    orders = OrderItems.objects.all().order_by('-id')
    datefrom = None
    dateto = None
    if request.method == 'POST':
        datefrom = request.POST['datefrom']
        dateto = request.POST['dateto']
        try:
            orders=OrderItems.objects.filter(updated_at__lte=dateto,updated_at__gte=datefrom).order_by('-id')
            context = {
                'orders':orders,
                'datef':datefrom,
                'datet':dateto,
            }
        except:
            pass
        return render(request,'sales_report.html',context)
    else:
        context = {
            'orders':orders,
            'datefrom':datefrom,
            'dateto':dateto,
        }
        return render(request,'sales_report.html',context)
