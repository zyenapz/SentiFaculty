from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def visualizer_home(request):
    context = {
        'title': "Visualizer dashboard",
    }
    return render(request, 'visualizer/visualizer_home.html', context)
