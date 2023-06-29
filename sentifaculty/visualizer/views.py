import plotly.express as px
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from feedback.models import Feedback
from visualizer.helpers.tables import FeedbackFilterSet
from visualizer.helpers.tables import FeedbackTable
from visualizer.models import FacultyEvaluation
from visualizer.helpers.charts_html import SF_SentipieHTML, SF_WordcloudHTML, SF_OverallWordcloudHTML, SF_OverallLinegraphHTML
from visualizer.helpers.comments import SF_BestComment, SF_WorstComment
from visualizer.helpers.reports import SF_CommentReport, SF_StrandReport, SF_SubjectReport, SF_FacultyRankings
from users.models import TEACHER, ADMIN, PRINCIPAL, Teacher
from visualizer.models import Subject, AcademicYear
from django.template.defaulttags import register

from wordcloud import WordCloud, STOPWORDS

from .forms import FEPeriodForm, SubjectSortForm

# User checks
def teacher_check(user):
    return user.user_type == TEACHER

def teacher_or_admin_check(user):
    return user.user_type == TEACHER or user.user_type == ADMIN

def admin_check(user):
    return user.user_type == ADMIN

# Create your views here.
@user_passes_test(teacher_check, login_url="login")
def visualizer_home(request):
    user_id = request.user.id
    check = get_object_or_404(Teacher, user__id=user_id)
    
    selected_fe = FacultyEvaluation.objects.filter(is_ongoing=True).first()
    if request.method == 'GET':
        selection = request.GET.get('fe', None)

        if selection:
            selected_fe = FacultyEvaluation.objects.filter(pk=selection).first()

    query_exists = Feedback.objects.filter(
        evaluatee__teacher__user__id=user_id,   
        evaluatee__fe=selected_fe
    ).exists()
 
    context = {
        'title': "Visualizer dashboard",
        'teacher': check,
        'query_exists': query_exists,
        'wordcloud': SF_WordcloudHTML(user_id, selected_fe),
        'chart': SF_SentipieHTML(request, user_id, selected_fe),
        'best_comment': SF_BestComment(user_id, selected_fe),
        'worst_comment': SF_WorstComment(user_id, selected_fe),
        'comment_report': SF_CommentReport(user_id, selected_fe),
        'strand_report': SF_StrandReport(user_id, selected_fe),
        'subject_report': SF_SubjectReport(user_id, selected_fe),
        'fe_select': FEPeriodForm(),
        'selected_fe': selected_fe,
    }

    return render(request, 'visualizer/home.html', context)

@user_passes_test(teacher_check, login_url="login")
def visualizer_comments(request):
    user_id = request.user.id

    selected_fe = FacultyEvaluation.objects.filter(is_ongoing=True).first()
    if request.method == 'GET':
        selection = request.GET.get('fe', None)

        if selection:
            selected_fe = FacultyEvaluation.objects.filter(pk=selection).first()

    feedbacks = Feedback.objects.filter(
        evaluatee__teacher__user__id=user_id,   
        evaluatee__fe=selected_fe
    )

    # FilterSet
    myFilter = FeedbackFilterSet(request.GET, queryset=feedbacks)
    feedbacks = myFilter.qs
    
    context = {
        'title': "Comments",
        'fe_select': FEPeriodForm(),
        'feedback_table': FeedbackTable(feedbacks),
        'query_exists': feedbacks.exists(),
        'selected_fe': selected_fe,
        'filter': myFilter,
    }
    return render(request, 'visualizer/comments.html', context)

@user_passes_test(admin_check, login_url="login")
def admin_home(request):
    context = {
        'title': "Admin Home",
        'admin': True,
        'rankings': SF_FacultyRankings(),
        'cloud': SF_OverallWordcloudHTML(),
    }
    return render(request, 'visualizer/home.html', context)

@user_passes_test(admin_check, login_url="login")
def admin_faculty_view(request, teacher_id):
    check = get_object_or_404(Teacher, user__id=teacher_id)
    teacher = teacher_id
    
    selected_fe = FacultyEvaluation.objects.filter(is_ongoing=True).first()
    if request.method == 'GET':
        selection = request.GET.get('fe', None)

        if selection:
            selected_fe = FacultyEvaluation.objects.filter(pk=selection).first()

    query_exists = Feedback.objects.filter(
        evaluatee__teacher__user__id=teacher,   
        evaluatee__fe=selected_fe
    ).exists()
 
    context = {
        'title': "Visualizer dashboard",
        'admin': True,
        'teacher': check,
        'query_exists': query_exists,
        'wordcloud': SF_WordcloudHTML(teacher, selected_fe),
        'chart': SF_SentipieHTML(request, teacher, selected_fe),
        'best_comment': SF_BestComment(teacher, selected_fe),
        'worst_comment': SF_WorstComment(teacher, selected_fe),
        'comment_report': SF_CommentReport(teacher, selected_fe),
        'strand_report': SF_StrandReport(teacher, selected_fe),
        'subject_report': SF_SubjectReport(teacher, selected_fe),
        'fe_select': FEPeriodForm(),
        'selected_fe': selected_fe,
    }

    return render(request, 'visualizer/home.html', context)

@user_passes_test(admin_check, login_url="login")
def admin_faculty_comments(request, teacher_id):
    check = get_object_or_404(Teacher, user__id=teacher_id)
    teacher = teacher_id

    selected_fe = FacultyEvaluation.objects.filter(is_ongoing=True).first()
    if request.method == 'GET':
        selection = request.GET.get('fe', None)

        if selection:
            selected_fe = FacultyEvaluation.objects.filter(pk=selection).first()

    feedbacks = Feedback.objects.filter(
        evaluatee__teacher__user__id=teacher,
        evaluatee__fe=selected_fe
    )

    # FilterSet
    myFilter = FeedbackFilterSet(request.GET, queryset=feedbacks)
    feedbacks = myFilter.qs
    
    context = {
        'title': "Comments",
        'admin': True,
        'teacher': check,
        'fe_select': FEPeriodForm(),
        'feedback_table': FeedbackTable(feedbacks),
        'query_exists': feedbacks.exists(),
        'selected_fe': selected_fe,
        'filter': myFilter,
    }
    return render(request, 'visualizer/comments.html', context)

@user_passes_test(admin_check, login_url="login")
def admin_faculty_history(request):
    context = {
        'title': 'Admin faculty history',
        'admin': True,
        'chart': SF_OverallLinegraphHTML(),
    }
    return render(request, 'visualizer/home.html', context)