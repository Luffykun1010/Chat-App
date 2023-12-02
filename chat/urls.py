from . import views
from django.urls import path,include
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('<slug:slug>',views.room,name='room'),
    path('login',views.loginpage,name='login'),
    path('signup',views.signuppage,name='signup'),
    path('logout',views.logoutpage,name='logout'),
]