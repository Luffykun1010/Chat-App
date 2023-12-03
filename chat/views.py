from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Room,Messages
def home(request):
    if request.user.is_authenticated:
        room=Room.objects.all()
        return render(request,'home.html',{'room':room})
    else:
        return redirect('login')
def signuppage(request):
    if request.method == 'POST':
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        myuser=User.objects.create(username=phone,password=password)
        myuser.save()
        return redirect('login')
    return render(request,'signup.html')
def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('phone')
        password=request.POST.get('password')
        myuser = authenticate(username=username,password=password)
        if myuser is not None:    
            login(request,myuser)
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('login')
    return render(request,'login.html')
def room(request,slug):
    if request.user.is_authenticated:
        rooms=Room.objects.get(slug=slug)
        messages=Messages.objects.filter(room=rooms)
        return render(request,'room.html',{'room':Room.objects.all(),'rooms':rooms,'message':messages})
    else:
        return redirect('login')