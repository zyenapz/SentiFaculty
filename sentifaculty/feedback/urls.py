from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback, name="student-feedback"),
    path('landing/', views.landing,name="landing-feedback"),
]
