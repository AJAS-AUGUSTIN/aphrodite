from itertools import product
import re
from django.db.models.aggregates import Count
from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User, auth
from django.db.models import Q
from orders.models import Order, OrderItems
from category.models import Categories, Products, SubCategories
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from accounts.models import Account
import datetime
import calendar
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#xhtml2pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
@never_cache
def adminlogin(request):
    all_order = Order.objects.all()
    net_profit=0
    for order in all_order:
        total=int(order.grand_total)
        net_profit += total 
    order = Order.objects.distinct('user')
    customer_count=0
    for ors in order:
        customer_count += 1
    order_items = OrderItems.objects.all()
    first=0
    date = datetime
    for ord in order_items:
        product_count = ord.quantity
        first += product_count

    #for chart
    orderitems = OrderItems.objects.annotate(month=ExtractMonth('updated_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber=[]
    totalOrders=[]
    for d in orderitems:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
        total_orders=OrderItems.objects.all().count()
        total_products=Products.objects.all().count()
        total_sale=OrderItems.objects.aggregate(Sum('grand_total'))
        category_list = SubCategories.objects.order_by('title').distinct('title')
        quantity_list=[]
        for k in category_list:
            product_list  =Products.objects.filter(SubCategories_id=k.id)
            quantity_sum=0
            for i in product_list:
                quantity = OrderItems.objects.filter(products_id=i.id)
                for j in quantity:
                    quantity_sum+=j.quantity
            quantity_list.append(quantity_sum)
        every_product = Products.objects.all()
       
    context = {
        'product_count':first,
        'date':date,
        'customer_count':customer_count,
        'net_profit':net_profit,
        'monthNumber':monthNumber,
        'totalOrders':totalOrders,

        'total_orders':total_orders,
        'total_products':total_products,
        'total_sale':total_sale,
        'category':category_list,
        'quantity':quantity_list,
        'product_list':every_product
    }
    if request.session.has_key('admin'):
        return render(request, 'adminmain.html',context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superadmin == True:
            request.session['admin'] = True
            auth.login(request, user)
            return render(request, 'adminmain.html',context)
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'adminlogin.html')
    else:
        return render(request, 'adminlogin.html')


def adminlogout(request):
    del request.session['admin']
    auth.logout(request)
    return redirect(adminlogin)


def deluser(request, id):
    try:
        user = Account.objects.get(id=id)
        user.delete()
        messages.sucess(request, "The user is deleted")
    except:
        messages.error(request, "The user not found")
    return redirect(adminhome)


def updateuser(request, id):
    user = Account.objects.get(id = id)
    if request.method == 'GET':
        return render(request, 'updateuser.html', {'user': user})
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        emaill = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
            
        if emaill != '':
           user.email = emaill
        if username != '':
            user.username = username
            user.save()
        return redirect('adminhome')


def statusupdate(requset,id):
    user = Account.objects.get(id = id)
    if user.is_active == True:
        user.is_active = False
        user.save()
        return redirect('adminhome')
    else:
        user.is_active = True
        user.save()
        return redirect('adminhome')


@never_cache
def adminhome(request):
    user = Account.objects.filter(is_superadmin = False)
    if request.session.has_key('admin'):
        if 'search' in request.POST:
            search = request.POST['search']
            user = Account.objects.filter( Q(username__icontains=search) | Q(first_name__icontains=search ))
            return render(request, 'adminhome.html', {'users': user})
        else:
            return render(request, 'adminhome.html', {'users': user})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser == True:
            request.session['admin'] = True
            auth.login(request, user)
            user = User.objects.filter(is_superuser = False)
            return render(request, 'adminhome.html', {'users': user})
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'adminlogin.html')
    else:
        return render(request, 'adminlogin.html')


def pdf_report(request):
    fromdate = request.POST.get('date1')
    todate = request.POST.get('date2')
    if fromdate and todate is not None:
        orders=OrderItems.objects.filter(updated_at__lte=todate,updated_at__gte=fromdate).order_by('-id')
    else:
        orders = OrderItems.objects.all().order_by('-id')
    template_path = 'pdf_sales_report.html'
    context = {'orders': orders}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="sales_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

