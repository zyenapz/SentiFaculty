from django.shortcuts import HttpResponseRedirect, render

from feedback.helpers.analyzer import SFAnalyzer, Sentiment
from .forms import FeedbackForm
from .models import AcademicYear, Feedback, SentimentScore, Student
from visualizer.models import Teacher

# Create your views here.
def feedback(request):

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)

            # TODO: THESE OBJECTS ARE DUMMY DATA ...
            # ... except for the sentiment scores
            new_feedback.teacher = Teacher.objects.get(pk=1)
            new_feedback.student = Student.objects.first()
            new_feedback.academic_year = AcademicYear.objects.first()

            # Calculate Vader, BERT and hybrid scores
            analyzer = SFAnalyzer()
            vader = analyzer.use_vader(new_feedback.comment)
            bert = analyzer.use_bert(new_feedback.comment)
            hybrid = analyzer.use_hybrid(new_feedback.comment)

            score = SentimentScore(
                vader_pos = vader.pos,
                vader_neg = vader.neg,
                bert_pos = bert.pos,
                bert_neg = bert.neg,
                hybrid_pos = hybrid.pos,
                hybrid_neg = hybrid.neg,
            )

            score.save()
            new_feedback.sentiment_score = score

            # Save form
            new_feedback.save()
            form.save_m2m()

    form = FeedbackForm()
    context = {
        'title': "Feedback",
        'form': form,
    }
        
    return render(request, 'feedback/feedback.html', context)
