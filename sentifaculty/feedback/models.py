from django.db import models
from django.utils.translation import gettext_lazy as _


class Section(models.Model):
    section_ID = models.CharField(max_length=3, primary_key=True)


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


class Student(models.Model):
    student_ID = models.CharField(max_length=10, primary_key=True)
    section_ID = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
        # NOTE WHAT TO DO ON DELETE?
    )
    strand_ID = models.ForeignKey(Strand, on_delete=models.PROTECT)
    email = models.EmailField()


class Feedback(models.Model):
    # NOTE We are creating the relationship on an as of yet undefined model https://docs.djangoproject.com/en/4.1/ref/models/fields/#lazy-relationships
    teacher_ID = models.ForeignKey('Teacher', on_delete=models.PROTECT)
    student_ID = models.ForeignKey(Student, on_delete=models.PROTECT)
    academic_year_ID = models.ForeignKey(
        'Academic_Year', on_delete=models.PROTECT)
    # FIXME min_length is not an accepted argument do we just enforce programatically? (10 char minimum)
    content = models.CharField(max_length=100)
    actual_sentiment = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)
    vader_senti_ID = models.ForeignKey(
        'VADER_Sentiment', on_delete=models.PROTECT)
    bert_senti_ID = models.ForeignKey(
        'BERT_Sentiment', on_delete=models.PROTECT)


class Academic_Year(models.Model):
    # FIXME How do we store the year values? The date field cannot store truncated values
    # so if we use the DateField() we must filter by year
    start_year = models.DateField()
    end_year = models.DateField()

class VADER_Sentiment(models.Model):
    positive_score=models.DecimalField(max_digits=4,decimal_places=2)
    negative_score=models.DecimalField(max_digits=4,decimal_places=2)

class BERT_Sentiment(models.Model):
    positive_score=models.DecimalField(max_digits=4,decimal_places=2)
    negative_score=models.DecimalField(max_digits=4,decimal_places=2)

# NOTE Which models should reside in the visualizer app?
# Teachers will be in users, alongside the admin but not as an administrator account
# Subject maybe? And then academic year remains here
# NOTE just restore from commit 7f736d238f6027af33925928e3b055358dce0b50 if this is really bad