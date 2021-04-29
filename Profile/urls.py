from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Profile import views

urlpatterns = [
    path('signin/', views.sign_in),
    path('signup/', views.sign_up),
    path('signout/', views.sign_out),
    path('<str:username>/',views.profile_page, name='profile'),
    path('<str:username>/update/profile/', views.update_profile),
    path('<str:username>/update/prf/', views.upd_profile),
]