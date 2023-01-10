from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_teacher, name="fb-select"),
    path('getfeedback', views.get_feedback, name="fb-getfb"),
]
