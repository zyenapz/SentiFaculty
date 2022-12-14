from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Section(models.Model):
    section_ID=models.CharField(max_length=3,primary_key=True)

# https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices 
# NOTE Used the 'choices' field option
class Strand(models.Model):
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
    
    strand_name=models.CharField(
        max_length=10,
        choices=StrandChoices.choices,
        default=StrandChoices.HUMSS,
    )

class Student(models.Model):
    student_ID=models.CharField(max_length=10)
    section_ID=models.ForeignKey(
        Section,
        on_delete=models.PROTECT
        # NOTE WHAT TO DO ON DELETE?
    )

class Feedback(models.Model):
    # NOTE We are creating the relationship on an as of yet undefined model https://docs.djangoproject.com/en/4.1/ref/models/fields/#lazy-relationships
    teacher_ID=models.ForeignKey('Teacher',on_delete=models.PROTECT)
    student_ID=models.ForeignKey(Student,on_delete=models.PROTECT)
    academic_year_ID=models.ForeignKey('Academic_Year',on_delete=models.PROTECT)
    # FIXME min_length is not an accepted argument do we just enforce programatically? (10 char minimum)
    content=models.CharField(max_length=100)
    actual_sentiment=models.CharField(max_length=20)
    submission_date=models.DateTimeField(auto_now_add=True)
    vader_senti_ID=models.ForeignKey('VADER_Sentiment',on_delete=models.PROTECT)
    bert_senti_ID=models.ForeignKey('BERT_Sentiment',on_delete=models.PROTECT)

# NOTE Which models should reside in the visualizer app?
# Teachers will be in users, alongside the admin but not as an administrator account
# Subject maybe? And then academic year remains here

# NOTE Retaining these because my changes might be hideous
""" class Student(models.Model):
    class Strand(models.TextChoices):
        ABM = "ABM"
        ABMB = "ABM-B"
        ABMBUS = "ABMBUS"
        HE = "HE"
        HUMS = "HUMS"
        HUMSS = "HUMSS"
        ICT = "ICT"
        STEM = "STEM"
        STEMM = "STEM-M"
        STEMS = "STEM-S"
        STEMB = "STEMB"
        STEMF = "STEMF"
        STEMG = "STEMG"
        STEMMA = "STEMMA"
        STEMSC = "STEMSC"

    class YearLevel(models.TextChoices):
        GRADE_11 = "11"
        GRADE_12 = "12"

    number = models.CharField(max_length=10) # TODO: Change max_length later if student numbers are different
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    # TODO: Normalize these later
    year_level = models.CharField(max_length=2, choices=YearLevel.choices, default=YearLevel.GRADE_11)
    section = models.CharField(max_length=3) 
    strand = models.CharField(max_length=10, choices=Strand.choices, default=Strand.ABM)

class Faculty(models.Model):
    number = models.CharField(max_length=10) # TODO: Change max_length later if faculty numbers are different
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Feedback(models.Model):
    class Sentiment(models.IntegerChoices):
        POSITIVE = 1
        NEUTRAL = 0
        NEGATIVE = -1

    content = models.CharField(max_length=100)
    actual_sentiment = models.IntegerField(choices=Sentiment.choices)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

class Course(models.Model):
    pass # TODO: Not sure if this is needed tho ... since we are just focusing on feedback and faculty """