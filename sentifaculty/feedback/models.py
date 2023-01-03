from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from visualizer.models import Teacher


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


class Feedback(models.Model):
    class SentimentChoice(models.TextChoices):
        POSITIVE = "POSITIVE", _('POSITIVE')
        NEUTRAL = "NEUTRAL", _('NEUTRAL')
        NEGATIVE = "NEGATIVE", _('NEGATIVE')

    content = models.TextField(max_length=100, validators=[
                               validators.MinLengthValidator(10)])
    actual_sentiment = models.CharField(
        max_length=10, choices=SentimentChoice.choices, default=SentimentChoice.NEUTRAL)

    # NOTE We are creating the relationship on an as of yet undefined model https://docs.djangoproject.com/en/4.1/ref/models/fields/#lazy-relationships
    teacher_ID = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    student_ID = models.ForeignKey(Student, on_delete=models.PROTECT)
    academic_year_ID = models.ForeignKey(
        'Academic_Year', on_delete=models.PROTECT)
    submission_date = models.DateTimeField(auto_now_add=True)
    vader_senti_ID = models.ForeignKey(
        'VADER_Sentiment', on_delete=models.PROTECT)
    bert_senti_ID = models.ForeignKey(
        'BERT_Sentiment', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.content


class Academic_Year(models.Model):
    # FIXME How do we store the year values? The date field cannot store truncated values
    # so if we use the DateField() we must filter by year
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self) -> str:
        # BUG need to test this, it might explode
        return f"{self.start_year.strftime('%Y')}-{self.end_year.strftime('%Y')}"


class VADER_Sentiment(models.Model):
    positive_score = models.DecimalField(max_digits=4, decimal_places=2)
    negative_score = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        # BUG test this too
        return f'POS:{self.positive_score} NEG:{self.negative_score}'


class BERT_Sentiment(models.Model):
    positive_score = models.DecimalField(max_digits=4, decimal_places=2)
    negative_score = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        # BUG test this too
        return f'POS:{self.positive_score} NEG:{self.negative_score}'