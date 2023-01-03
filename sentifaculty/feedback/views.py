from django.shortcuts import render
from .forms import FeedbackForm

# Create your views here.
def feedback(request):
    context = {
        'title': "Feedback",
        'form': FeedbackForm,
    }
    return render(request, 'feedback/feedback.html', context)
