from django.shortcuts import render
from .forms import FeedbackForm
from .models import AcademicYear, Teacher

# Create your views here.
def feedback(request):

    if request.method == "POST":
        # print(request.POST)
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.academic_year_ID = AcademicYear.objects.get(start_year=2022)
            form.teacher_id = Teacher.objects.get(pk=1)

            form.save()

            #return HttpResponseRedirect('')
    
    else:
        form = FeedbackForm()

        context = {
            'title': "Feedback",
            'form': form,
        }
    
    return render(request, 'feedback/feedback.html', context)
