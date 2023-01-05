from django.shortcuts import HttpResponseRedirect, render
from .forms import FeedbackForm
from .models import AcademicYear, BertSentiment, Feedback, Student, VaderSentiment
from visualizer.models import Teacher

# Create your views here.
def feedback(request):

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.teacher = Teacher.objects.get(pk=1)
            new_feedback.student = Student.objects.first()
            new_feedback.academic_year = AcademicYear.objects.first()
            new_feedback.vader = VaderSentiment.objects.first()
            new_feedback.bert = BertSentiment.objects.first()

            new_feedback.save()
            form.save_m2m()

    form = FeedbackForm()
    context = {
        'title': "Feedback",
        'form': form,
    }
        
    return render(request, 'feedback/feedback.html', context)
