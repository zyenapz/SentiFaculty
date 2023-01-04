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
        elif self.end_year <= self.start_year:
            raise ValidationError("'End year' must not be equal or earlier than the 'Start year'")

class Feedback(models.Model):
    class SentimentChoice(models.TextChoices):
        POSITIVE = "POSITIVE", _('POSITIVE')
        NEUTRAL = "NEUTRAL", _('NEUTRAL')
        NEGATIVE = "NEGATIVE", _('NEGATIVE')

    content = models.TextField(max_length=100, validators=[
                               validators.MinLengthValidator(10)])
    actual_sentiment = models.CharField(
        max_length=10, choices=SentimentChoice.choices, default=SentimentChoice.NEUTRAL)
    submission_date = models.DateTimeField(auto_now_add=True)

    # NOTE We are creating the relationship on an as of yet undefined model https://docs.djangoproject.com/en/4.1/ref/models/fields/#lazy-relationships
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    vader = models.ForeignKey(
        'VaderSentiment', on_delete=models.PROTECT)
    bert = models.ForeignKey(
        'BertSentiment', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.content

class VaderSentiment(models.Model):
    positive_score = models.DecimalField(max_digits=4, decimal_places=2)
    negative_score = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        # BUG test this too
        return f'POS:{self.positive_score} NEG:{self.negative_score}'


class BertSentiment(models.Model):
    positive_score = models.DecimalField(max_digits=4, decimal_places=2)
    negative_score = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        # BUG test this too
        return f'POS:{self.positive_score} NEG:{self.negative_score}'