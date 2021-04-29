from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/<str:contest>/', views.register),
    path('schedules/', views.schedule),
]