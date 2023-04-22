from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Not a valid User')
            return redirect('/eauth/signin')
    else:
        return render(request, "eauth/signin.html")

def signup(request):
    if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        password2=request.POST.get("password2")
        
        if password==password2:
            if User.objects.filter(email__icontains=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('/eauth/signup/')
            elif User.objects.filter(username__icontains=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('/eauth/signup/')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                auth.login(request,user)
                return redirect('/')
        else:
            messages.info(request,'Password do not match')
            return redirect('/eauth/signup/')
    else:
        return render(request, 'eauth/signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/eauth/signin')