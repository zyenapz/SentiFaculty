from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_teacher, name="fb-select"),
    path('getfeedback', views.get_feedback, name="fb-getfb"),
    path('todo', views.todo_page, name="todo-page")
]
