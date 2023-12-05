from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import ChatMessage,Thread
from django.db.models import Q
def home(request):
    if request.user.is_authenticated:
        threads=Thread.objects.by_user(user=request.user)
        context = {
            'Threads': threads,
        }
        return render(request,'home.html',context)
    else:
        return redirect('login')
def signuppage(request):
    if request.method == 'POST':
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        myuser=User.objects.create_user(phone,email,password)
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
        threads=Thread.objects.by_user(user=request.user)
        message = ChatMessage.objects.filter(Q(sended_by=request.user) | Q(sended_to=request.user)).order_by('timestamp')
        context = {
            'Threads': threads,
            'message':message,
        }
        return render(request,'chat.html',context)
    else:
        return redirect('login')