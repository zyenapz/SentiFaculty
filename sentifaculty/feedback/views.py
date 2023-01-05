from django.shortcuts import HttpResponseRedirect, render
from .forms import FeedbackForm
from .models import AcademicYear, BertSentiment, Feedback, Student, VaderSentiment
from visualizer.models import Teacher
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pysentimiento import create_analyzer

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

    bert = create_analyzer(task="sentiment", lang="en")
    print(bert.predict("I like you!"))

    vader = SentimentIntensityAnalyzer()
    print(vader.polarity_scores("I like you!"))
        
    return render(request, 'feedback/feedback.html', context)
