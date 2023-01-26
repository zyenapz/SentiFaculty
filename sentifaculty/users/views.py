from django.shortcuts import render
from django.contrib.auth.views import login

# Create your views here.
def sf_login(request):
    if request.user.is_authenticated:
        pass 
    else: 
        return login(request)