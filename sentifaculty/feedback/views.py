from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from feedback.helpers.analyzer import SFAnalyzer
from users.models import Teacher, Student, STUDENT, ADMIN
from .forms import FeedbackForm, SelectTeacherForm
from .models import AcademicYear, SentimentScore

# NOTE (@login_required decorator)
# NOTE https://docs.djangoproject.com/en/4.1/topics/auth/default/ 

def student_check(user):
    # TODO remove admin later
    return user.user_type == STUDENT or user.user_type == ADMIN

@user_passes_test(student_check, login_url="todo-page")
def get_feedback(request):

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)

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

            # TODO: THESE OBJECTS ARE DUMMY DATA ...
            # ... except for the sentiment scores
            new_feedback.teacher = Teacher.objects.get(pk=1)
            new_feedback.student = Student.objects.first()
            new_feedback.academic_year = AcademicYear.objects.first()

            # Save form
            new_feedback.save()
            form.save_m2m()

    form = FeedbackForm()
    context = {
        'title': "Feedback",
        'form': form,
    }
        
    return render(request, 'feedback/feedback.html', context)

@user_passes_test(student_check, login_url="todo-page")
def select_teacher(request):
    form = SelectTeacherForm()

    context = {'form': form}
    return render(request, 'feedback/select.html', context)    

# TODO Construct a proper redirect url later depending on whether or not ...
# ... a user has logged in as student, teacher, or principal
def todo_page(request):
    return HttpResponse("<html><body>Under construction. You are not logged in as a student nor admin.</body></html>")