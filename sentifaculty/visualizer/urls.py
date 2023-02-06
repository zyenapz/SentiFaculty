from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.visualizer_home, name="visualizer-home"),
    path('linegraph/', views.visualizer_linegraph, name='linegraph'),
    path('comments', views.visualizer_comments, name='visualizer-comments'),

    path('dashboard/',views.visualizer_dashboard,name='dashboard'),
    path('wordcloud/',views.visualizer_wordcloud,name='wordcloud'),

    path('login/', auth_views.LoginView.as_view(template_name='visualizer/login.html',
         extra_context={'title': "Visualizer login"}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='visualizer/logout.html',
         extra_context={'title': "Visualizer logout"}), name='logout'),     

]
