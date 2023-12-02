from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Room
def home(request):
    if request.user.is_authenticated:
        room=Room.objects.all()
        return render(request,'home.html',{'room':room})
    else:
        return redirect('login')
def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('phone')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:    
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('login')
    return render(request,'login.html')
def signuppage(request):
    if request.method == 'POST':
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        myuser=User.objects.create(username=phone,password=password)
        myuser.save()
        return redirect('login')
    return render(request,'signup.html')
def logoutpage(request):
    logout(request)
    return redirect('login')
def room(request,slug):
    return render(request,'room.html',{'room':Room.objects.all(),'rooms':Room.objects.filter(slug=slug)})