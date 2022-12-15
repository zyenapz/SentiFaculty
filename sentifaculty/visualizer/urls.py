from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizer_login, name="visualizer-login")
]
