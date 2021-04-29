from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Contest import views

urlpatterns = [
    path('page/<str:Name>/', views.contest, name='contest'), 
]