from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackSectionForm, FeedbackStrandForm, FeedbackStudentForm

# Create your views here.


def feedback(request):
    context = {
        'title': "Feedback",
    }
    return render(request, 'feedback/feedback.html', context)


def landing(request):
    # FIXME INCOMPLETE IMPLEMENTATION, requires some kind of session storage data for
    # the student, and to check if the inputted student data already exists (CREATE IF NOT EXISTS or whatever)
    if request.method == 'POST':
        section_form = FeedbackSectionForm(request.POST)
        strand_form = FeedbackStrandForm(request.POST)
        student_form = FeedbackStudentForm(request.POST)
        if section_form.is_valid() and strand_form.is_valid() and student_form.is_valid():
            section_form.save()
            strand_form.save()
            student_form.save()
            messages.success(request, 'Redirecting to feedback page')
            return redirect('student-feedback')
    else:
        section_form = FeedbackSectionForm()
        strand_form = FeedbackStrandForm()
        student_form = FeedbackStudentForm()
    context = {
        'section_form': section_form,
        'strand_form': strand_form,
        'student_form': student_form,
    }
    return render(request, 'feedback/landing.html', context)
