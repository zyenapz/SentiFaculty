from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from visualizer.models import Teacher
from django.core.exceptions import ValidationError

class Section(models.Model):
    section_ID = models.CharField(max_length=3, primary_key=True)

    def __str__(self) -> str:
        return self.section_ID


class Strand(models.Model):
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices
    # NOTE Used the 'choices' field option
    class StrandChoices(models.TextChoices):
        ABM = "ABM", _('ABM')
        ABMB = "ABM-B", _('ABM-B')
        ABMBUS = "ABMBUS", _('ABMBUS')
        HE = "HE", _('HE')
        HUMS = "HUMS", _('HUMS')
        HUMSS = "HUMSS", _('HUMSS')
        ICT = "ICT", _('ICT')
        STEM = "STEM", _('STEM')
        STEMM = "STEM-M", _('STEM-M')
        STEMS = "STEM-S", _('STEM-S')
        STEMB = "STEMB", _('STEMB')
        STEMF = "STEMF", _('STEMF')
        STEMG = "STEMG", _('STEMG')
        STEMMA = "STEMMA", _('STEMMA')
        STEMSC = "STEMSC", _('STEMSC')

    strand_name = models.CharField(
        max_length=10,
        choices=StrandChoices.choices,
        default=StrandChoices.HUMSS,
    )

    def __str__(self) -> str:
        return self.strand_name


class Student(models.Model):
    student_ID = models.CharField(max_length=10, primary_key=True)
    section_ID = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )
    strand_ID = models.ForeignKey(Strand, on_delete=models.PROTECT)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.student_ID


class AcademicYear(models.Model):
    start_year = models.PositiveIntegerField(primary_key=True)
    end_year = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def clean(self):
        if self.start_year >= self.end_year:
            raise ValidationError("'Start year' must not be equal or later than the 'End year'")
        if self.end_year != self.start_year + 1:
            raise ValidationError("'End year' can only be 1 year later than 'Start year'")

class SentimentScore(models.Model):
    MAX_DIGITS = 4
    MAX_DECIMAL = 2

    vader_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    vader_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)

class Feedback(models.Model):
    class SentimentChoice(models.TextChoices):
        POSITIVE = "POSITIVE", _('POSITIVE')
        NEUTRAL = "NEUTRAL", _('NEUTRAL')
        NEGATIVE = "NEGATIVE", _('NEGATIVE')

    comment = models.TextField(max_length=100, validators=[
                               validators.MinLengthValidator(10)])
    actual_sentiment = models.CharField(
        max_length=10, choices=SentimentChoice.choices, default=SentimentChoice.NEUTRAL)
    submission_date = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    sentiment_score = models.ForeignKey(SentimentScore, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.comment