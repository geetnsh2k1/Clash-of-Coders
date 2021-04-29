from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Submission import views

urlpatterns = [
    path('<str:Name>/', views.submission), 
]