from django.shortcuts import render

# Create your views here.
def feedback(request):
    context = {
        'title': "Feedback",
    }
    return render(request, 'feedback/feedback.html', context)
