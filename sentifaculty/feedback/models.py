from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Student, Teacher 
from visualizer.models import AcademicYear

class SentimentChoice(models.TextChoices):
    POSITIVE = "POSITIVE", _('POSITIVE')
    NEUTRAL = "NEUTRAL", _('NEUTRAL')
    NEGATIVE = "NEGATIVE", _('NEGATIVE')

class Feedback(models.Model):

    comment = models.TextField(max_length=100, validators=[
                               validators.MinLengthValidator(10)])
    actual_sentiment = models.CharField(
        max_length=10, choices=SentimentChoice.choices, default=SentimentChoice.NEUTRAL)
    submission_date = models.DateTimeField(auto_now_add=True)

    evaluatee = models.ForeignKey('Evaluatee', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    sentiment_score = models.ForeignKey('SentimentScore', on_delete=models.CASCADE)
    faculty_eval = models.ForeignKey('visualizer.FacultyEvaluation', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment

    def clean(self) -> str:
        # TODO add validation to ensure that a 'Student' can only submit one entry for every 'Evaluatee'
        pass

class SentimentScore(models.Model):
    MAX_DIGITS = 4
    MAX_DECIMAL = 2

    vader_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    vader_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)

class Evaluatee(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey('visualizer.Subject', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"({self.subject.subject_code}) {self.teacher}"

class HistoricalFeedback(models.Model):
    comment = models.TextField(max_length=100, validators=[
                               validators.MinLengthValidator(10)])
    actual_sentiment = models.CharField(
        max_length=10, choices=SentimentChoice.choices, default=SentimentChoice.NEUTRAL)
    submission_date = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    faculty_eval = models.ForeignKey('visualizer.FacultyEvaluation', on_delete=models.CASCADE)
    sentiment_score = models.ForeignKey(SentimentScore, on_delete=models.CASCADE)

