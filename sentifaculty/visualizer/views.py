import plotly.express as px
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from feedback.models import Feedback
from visualizer.models import FacultyEvaluation
from visualizer.helpers.charts_html import SF_SentipieHTML, SF_WordcloudHTML
from visualizer.helpers.comments import SF_BestComment, SF_WorstComment
from visualizer.helpers.reports import SF_CommentReport, SF_StrandReport, SF_SubjectReport
from users.models import TEACHER, ADMIN
from visualizer.models import Subject, AcademicYear
from django.template.defaulttags import register

from wordcloud import WordCloud, STOPWORDS

from .forms import SubjectSortForm

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
    faculty_eval = FacultyEvaluation.objects.get() # TODO: Use currently selected FE period
 
    context = {
        'title': "Visualizer dashboard",
        'wordcloud': SF_WordcloudHTML(user_id, faculty_eval),
        'chart': SF_SentipieHTML(request, user_id, faculty_eval),
        'best_comment': SF_BestComment(user_id, faculty_eval),
        'worst_comment': SF_WorstComment(user_id, faculty_eval),
        'comment_report': SF_CommentReport(user_id, faculty_eval),
        'strand_report': SF_StrandReport(user_id, faculty_eval),
        'subject_report': SF_SubjectReport(user_id, faculty_eval),
    }

    return render(request, 'visualizer/home.html', context)

# FIXME take the current teacher from request.user.id or whatever
# NOTE this implementation is included in both admin and faculty views
@user_passes_test(teacher_check, login_url="login")
def visualizer_dashboard(request):
    user_id = request.user.id
    data = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)
    subjects = Subject.objects.filter(
        evaluatee__teacher__user__id=user_id)
    section = request.GET.get('subject')
    if section:
        data = Feedback.objects.filter(evaluatee__subject__id=section)

    fig = px.pie(
        values=[
            len(data.filter(comment__sentiment_score__hybrid_pos__gt=0.00)),
            len(data.filter(comment__sentiment_score__hybrid_neg__gt=0.00)),
        ],
        names=['positive', 'negative'],
        title='Sentiment Rating',
        color=['positive', 'negative'],
        color_discrete_map={
            'positive': 'green',
            'negative': 'red',
        }
    )
    chart = fig.to_html()
    context = {'chart': chart,
               'form': SubjectSortForm(choices=[(entry.id, entry.subject_name) for entry in subjects])}
    return render(request, 'visualizer/chart.html', context)

# NOTE this is overall polarity rating history for individual faculty member
# this can be viewed by administrator
def visualizer_linegraph(request):
    # TODO change teacher to current selected teacher
    teacher=2019151001
    years = AcademicYear.objects.all()
    sentimentRating=[]
    for year in years:
        if len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(comment__sentiment_score__hybrid_pos__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher)) > len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(comment__sentiment_score__hybrid_neg__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher)):
            sentimentRating.append(2)
        elif len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(comment__sentiment_score__hybrid_pos__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher)) < len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(comment__sentiment_score__hybrid_neg__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher)):
            sentimentRating.append(0)
        else:
            sentimentRating.append(1)
    fig = px.line(
        # maybe use order_by on year?
        x = [str(year) for year in years],
        y = sentimentRating,
        title = 'History of overall sentiment polarity',
        labels = dict(x ='Academic Year',y = 'Sentiment polarity'),
    )
    fig.update_yaxes(dtick=1,tickvals=[0,1,2],ticktext=['Negative','Neutral','Positive'],range=[0,2])
    chart = fig.to_html()
    context = {'chart':chart}
    return render(request, 'visualizer/chart.html', context)

# NOTE The wordcloud should be available for admin accounts
def visualizer_wordcloud(request):
    # TODO need selected teacher for query
    data = Feedback.objects.filter(evaluatee__teacher__user__mcl_id=2019151001)
    words=''.join([str(entry.comment) for entry in data])
    cloud=WordCloud(stopwords=STOPWORDS).generate(words).to_svg()
    context = {
        'wordcloud':cloud,
    }
    return render(request, 'visualizer/chart.html', context)