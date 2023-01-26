from django.apps import apps
from django.contrib import admin

from .models import Comment, Evaluatee, Evaluator, Feedback, SentimentScore

# Admin displays
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['id', 'comment', 'evaluatee', 'evaluator', 'submit_date']
    list_filter = ['evaluatee', 'evaluator', 'submit_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id', 'text', 'actual_sentiment']
    list_filter = ['id', 'text', 'actual_sentiment']

@admin.register(SentimentScore)
class SentimentScoreAdmin(admin.ModelAdmin):
    model = SentimentScore
    list_display = ['id', 'vader_pos', 'vader_neg', 'bert_pos', 'bert_neg', 'hybrid_pos', 'hybrid_neg']
    list_filter = ['id', 'vader_pos', 'vader_neg', 'bert_pos', 'bert_neg', 'hybrid_pos', 'hybrid_neg']

@admin.register(Evaluatee)
class EvaluateeAdmin(admin.ModelAdmin):
    model = Evaluatee
    list_display = ['id', 'teacher', 'subject', 'fe']
    list_filter = ['id', 'teacher', 'subject', 'fe']

@admin.register(Evaluator)
class EvaluatorAdmin(admin.ModelAdmin):
    model = Evaluator
    list_display = ['id', 'section', 'strand', 'year_level', 'fe', 'student']
    list_filter = ['id', 'section', 'strand', 'year_level', 'fe', 'student']
