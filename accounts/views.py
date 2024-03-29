from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):

    if request.method== 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        password= request.POST['password']
        re_password= request.POST['re_password']
        email= request.POST['email']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user= User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created');
                return redirect('login')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')
        
    return render(request, 'register.html')

def login(request):

    if request.method== 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # return redirect('/')
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Incorrect password.')
            return redirect('login')
    else: 
        return render(request, 'login.html')

def logout(request): 
    auth.logout(request)
    return redirect('/')

def forgotpassword(request):
    return render(request, 'forgot-password.html')

@login_required(login_url="/accounts/login")
def profile(request):
    return render(request, 'profile.html')