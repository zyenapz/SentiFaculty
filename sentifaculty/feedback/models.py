from django.db import models

# Create your models here.
class Student(models.Model):
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
    pass # TODO: Not sure if this is needed tho ... since we are just focusing on feedback and faculty