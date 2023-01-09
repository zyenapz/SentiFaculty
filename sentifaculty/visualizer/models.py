from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re

class Subject(models.Model):
    subject_id = models.CharField(max_length=10, primary_key=True)
    subject_name = models.CharField(max_length=250, default='subj')

    teacher_ID = models.ForeignKey("users.Teacher", on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.subject_name

class Section(models.Model):
    section_ID = models.CharField(max_length=3, primary_key=True)

    def __str__(self) -> str:
        return self.section_ID

class Strand(models.Model):
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices
    # NOTE Used the 'choices' field option
    # class StrandChoices(models.TextChoices):
    #     ABM = "ABM", _('ABM')
    #     ABMB = "ABM-B", _('ABM-B')
    #     ABMBUS = "ABMBUS", _('ABMBUS')
    #     HE = "HE", _('HE')
    #     HUMS = "HUMS", _('HUMS')
    #     HUMSS = "HUMSS", _('HUMSS')
    #     ICT = "ICT", _('ICT')
    #     STEM = "STEM", _('STEM')
    #     STEMM = "STEM-M", _('STEM-M')
    #     STEMS = "STEM-S", _('STEM-S')
    #     STEMB = "STEMB", _('STEMB')
    #     STEMF = "STEMF", _('STEMF')
    #     STEMG = "STEMG", _('STEMG')
    #     STEMMA = "STEMMA", _('STEMMA')
    #     STEMSC = "STEMSC", _('STEMSC')

    # strand_name = models.CharField(
    #     max_length=10,
    #     choices=StrandChoices.choices,
    #     default=StrandChoices.HUMSS,
    #     primary_key=True
    # )

    strand_name = models.CharField(max_length=8, primary_key=True)

    def __str__(self) -> str:
        return self.strand_name

    def clean(self):
        # RegEx Patterns
        pat_alphadash = re.compile(r"^[A-Z\-]+$")

        if not pat_alphadash.match(self.strand_name):
            raise ValidationError("Only CAPITALIZED alphabetic characters and dashes are accepted. No spaces allowed.")
        if self.strand_name.startswith("-") or self.strand_name.endswith("-"):
            raise ValidationError("Input cannot start or end with a dash.")

class AcademicYear(models.Model):
    start_year = models.PositiveIntegerField(primary_key=True)
    end_year = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def clean(self):
        if self.start_year >= self.end_year:
            raise ValidationError("'Start year' must not be equal or later than the 'End year'.")
        if self.end_year != self.start_year + 1:
            raise ValidationError("'End year' can only be 1 year later than 'Start year'.")
