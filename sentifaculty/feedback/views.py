from django.shortcuts import render
from .forms import FeedbackForm
from .models import AcademicYear

# Create your views here.
def feedback(request):


    if request.method == "POST":
        # print(request.POST)
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = FeedbackForm()
        context = {
            'title': "Feedback",
            'form': form,
        }
        
    return render(request, 'feedback/feedback.html', context)
