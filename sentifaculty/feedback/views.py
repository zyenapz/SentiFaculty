from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.db import transaction

from feedback.helpers.analyzer import SFAnalyzer
from users.models import Teacher, Student, STUDENT, ADMIN
from visualizer.models import FacultyEvaluation
from .forms import CommentForm, SelectEvaluateeForm
from .models import SentimentScore, Evaluatee, Feedback, Comment, Evaluator, Evaluatee

# User tests ----------------------------------------------------
# NOTE (@login_required decorator)
# NOTE https://docs.djangoproject.com/en/4.1/topics/auth/default/ 
def student_check(user):
    # TODO remove admin later
    return user.user_type == STUDENT or user.user_type == ADMIN

# Helpers -------------------------------------------------------
def calc_sentiment(text):
    # Calculate Vader, BERT and hybrid scores
    analyzer = SFAnalyzer()
    vader = analyzer.use_vader(text)
    bert = analyzer.use_bert(text)
    hybrid = analyzer.use_hybrid(text)

    score = SentimentScore(
        vader_pos = vader.pos,
        vader_neg = vader.neg,
        bert_pos = bert.pos,
        bert_neg = bert.neg,
        hybrid_pos = hybrid.pos,
        hybrid_neg = hybrid.neg,
    )

    return score

# Views ---------------------------------------------------------
@user_passes_test(student_check, login_url="todo-page")
def get_feedback(request):
    # Get selected evaluatee from session data
    evaluatee = next(
        serializers.deserialize(
            "json", 
            request.session.get('selected_evaluatee', None)
        )
    ).object

    # Process form
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            # Process comment
            comment = form.save(commit=False)
            score = calc_sentiment(comment.text)
            comment.sentiment_score = score

            # Process evaluator
            student = request.user.student
            evaluator = Evaluator(
                section=student.section,
                strand=student.strand,
                year_level=student.year_level,
                fe=FacultyEvaluation.objects.first(), # TODO dummy data
                student=student,
            )
            
            # Process feedback
            feedback = Feedback(
                evaluatee=evaluatee,
                evaluator=evaluator,
                comment=comment,
            )

            # Save objects
            try:
                with transaction.atomic():
                    score.save()
                    comment.save()
                    evaluator.save()
                    feedback.save()

            except IntegrityError:
                print("Something went wrong")

            return redirect('fb-select')       

    else:
        form = CommentForm()
        form.fields['actual_sentiment'].initial = None

    context = {
        'title': "Get Feedback",
        'form': form,
        'navbar_name': "getfeedback",
        'evaluatee': evaluatee,
    }
        
    return render(request, 'feedback/getfeedback.html', context)

@user_passes_test(student_check, login_url="todo-page")
def select_teacher(request):

    if request.method == "POST":
        form = SelectEvaluateeForm(request.POST)

        if form.is_valid():
            selected_evaluatee = form.cleaned_data['evaluatee']
            request.session['selected_evaluatee'] = serializers.serialize('json', [selected_evaluatee])
            return redirect('fb-getfb')  

    else:
        user = request.user.student
        #query = Evaluatee.objects.all()
        form = SelectEvaluateeForm()
        feedbacks = Feedback.objects.filter(evaluator__student=user)
        already_evaluated = list()

        # print(f"Hey:::: {feedbacks.first().evaluatee}")
        # print(f"ALO:::: {form['evaluatee'].field.queryset}")

        for feedback in feedbacks:
            for evaluatee in form.query:

                if feedback.evaluatee == evaluatee:
                    already_evaluated.append(evaluatee)
                else:
                    print("No match!")

        user_subjects = request.user.student.subjects.all()
        print(user_subjects)

    context = {
        'title': "Select Faculty",
        'form': form, 
        'navbar_name': "select",
        'already_evaluated': already_evaluated
    }
    return render(request, 'feedback/select.html', context)    

# TODO Construct a proper redirect url later depending on whether or not ...
# ... a user has logged in as student, teacher, or principal
def todo_page(request):
    # return HttpResponse("<html><body>Under construction. You are not logged in as a student nor admin.</body></html>")
    context = {'wip_name': "Visualizer"}
    return render(request, 'wip.html', context)