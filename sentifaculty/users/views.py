from django.shortcuts import redirect, render
from django.contrib.auth import login
from users.models import PRINCIPAL
from users.models import STUDENT, ADMIN, TEACHER

# Create your views here.

def sf_login(request):
    if not request.user.is_authenticated:
        pass
    else: 
        return login(request)
    
def login_redirect(request):
    user_type = request.user.user_type

    if user_type == STUDENT:
        return redirect("fb-select")
    elif user_type == TEACHER:
        return redirect("visualizer-home")
    elif user_type == ADMIN:
        return redirect("admin-home")
    else:
        return redirect("todo-page")
