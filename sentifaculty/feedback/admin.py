from django.apps import apps
from django.contrib import admin

from .models import Evaluatee, Feedback, SentimentScore

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['id', 'comment', 'evaluatee', 'student', 'actual_sentiment', 'submission_date']
    # list_filter = ['teacher', 'actual_sentiment', 'academic_year', 'submission_date']

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(SentimentScore)
admin.site.register(Evaluatee)
