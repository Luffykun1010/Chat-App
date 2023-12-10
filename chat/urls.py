from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('signup',views.signuppage,name='signup'),
    path('login',views.loginpage,name='login'),
    path('logout',views.logoutpage,name='logout'),
    path('<slug:slug>',views.room,name='room'),
]