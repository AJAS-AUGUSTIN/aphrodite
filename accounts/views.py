from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User, auth

from accounts.models import Account

# Create your views here.
@never_cache
def adminlogin(request):
    if request.session.has_key('admin'):
        print('index req received')
        return render(request, 'adminmain.html')
    elif request.method == 'POST':
        print('index POST req received')
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_superadmin == True:
            request.session['admin'] = True
            auth.login(request, user)
            return render(request, 'adminmain.html')
        else:
            print('else case')
            print('username and password not verified')
            messages.info(request, 'Invalid Credentials')
            return render(request, 'adminlogin.html')
    else:
        print('index GET req received')
        return render(request, 'adminlogin.html')

def adminadduser(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("username taken")
                messages.info(request, 'Username Taken')
                return redirect(adminadduser)
            elif User.objects.filter(email=email).exists():
                print("email taken")
                messages.info(request, 'E-mail Taken')
                return redirect(adminadduser)
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("usercreated")
                return redirect('adminlogin')

        else:
            print("Password not matching")
            messages.info(request, 'Passwords Not Matching')
            return redirect('adminadduser')
        # return redirect('/')
    else:
        return render(request, 'adminregistration.html')

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



def adminhome(request):
    user = Account.objects.filter(is_superadmin = False)
    # serializer = MessageSerializer(qs, many=True, context={'user': user})
    if request.session.has_key('admin'):
        print('index req received')
        if 'search' in request.POST:
            search = request.POST['search']
            user = Account.objects.filter(username__icontains=search)
            return render(request, 'adminhome.html', {'users': user})
        else:
            return render(request, 'adminhome.html', {'users': user})
    elif request.method == 'POST':
        print('index POST req received')
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_superuser == True:
            request.session['admin'] = True
            auth.login(request, user)
            user = User.objects.filter(is_superuser = False)
            return render(request, 'adminhome.html', {'users': user})
        else:
            print('else case')
            print('username and password not verified')
            messages.info(request, 'Invalid Credentials')
            return render(request, 'adminlogin.html')
    else:
        print('index GET req received')
        return render(request, 'adminlogin.html')

