from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.visualizer_home, name="visualizer-home"),
    path('comments/', views.visualizer_comments, name='visualizer-comments'),
    path('admin-home/', views.admin_home, name='admin-home'),
    path('admin-history/', views.admin_faculty_history, name='admin-history'),
    path('admin-faculty/<int:teacher_id>', views.admin_faculty_view, name='admin-faculty-view'),
    path('admin-faculty-comments/<int:teacher_id>', views.admin_faculty_comments, name='admin-faculty-comments'),

    path('login/', auth_views.LoginView.as_view(template_name='visualizer/login.html',
         extra_context={'title': "Visualizer login"}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='visualizer/logout.html',
         extra_context={'title': "Visualizer logout"}), name='logout'),     

]
