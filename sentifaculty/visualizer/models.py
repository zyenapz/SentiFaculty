from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re

class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    subject_name = models.CharField(max_length=250, default='Subject')

    def __str__(self) -> str:
        return f"({self.subject_code}) {self.subject_name}"

    def clean(self):
        pass 

class Section(models.Model):
    section_ID = models.CharField(max_length=3, unique=True)

    def __str__(self) -> str:
        return self.section_ID

class Strand(models.Model):
    class StrandChoices(models.TextChoices):
        STEM = "STEM", _('STEM')
        ABM = "ABM", _('ABM')
        HUMSS = "HUMSS", _('HUMSS')
        ICT = "ICT", _('ICT')
        # ABMB = "ABM-B", _('ABM-B')
        # ABMBUS = "ABMBUS", _('ABMBUS')
        # HE = "HE", _('HE')
        # HUMS = "HUMS", _('HUMS')
        # STEMM = "STEM-M", _('STEM-M')
        # STEMS = "STEM-S", _('STEM-S')
        # STEMB = "STEMB", _('STEMB')
        # STEMF = "STEMF", _('STEMF')
        # STEMG = "STEMG", _('STEMG')
        # STEMMA = "STEMMA", _('STEMMA')
        # STEMSC = "STEMSC", _('STEMSC')

    strand_name = models.CharField(
        max_length=10,
        choices=StrandChoices.choices,
        default=StrandChoices.HUMSS,
        unique=True,
    )

    def __str__(self) -> str:
        return self.strand_name

    def clean(self):
        pass
        # # RegEx Patterns
        # pat_alphadash = re.compile(r"^[A-Z\-]+$")

        # if not pat_alphadash.match(self.strand_name):
        #     raise ValidationError("Only CAPITALIZED alphabetic characters and dashes are accepted. No spaces allowed.")
        # if self.strand_name.startswith("-") or self.strand_name.endswith("-"):
        #     raise ValidationError("Input cannot start or end with a dash.")

class YearLevel(models.Model):
    class YearLevelChoices(models.TextChoices):
        GRADE_11 = "Grade 11", _("Grade 11")
        GRADE_12 = "Grade 12", _("Grade 12")

    level = models.CharField(choices=YearLevelChoices.choices, unique=True, max_length=10)

    def __str__(self) -> str:
        return self.level

class AcademicYear(models.Model):
    start_year = models.PositiveIntegerField(primary_key=True)
    end_year = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.start_year}-{self.end_year}"

    def clean(self):
        if self.start_year >= self.end_year:
            raise ValidationError("'Start year' must not be equal or later than the 'End year'.")
        if self.end_year != self.start_year + 1:
            raise ValidationError("'End year' can only be 1 year later than 'Start year'.")

class FacultyEvaluation(models.Model):
    academic_year = models.OneToOneField('AcademicYear', on_delete=models.CASCADE)
    is_ongoing = models.BooleanField(default=False)

    def __str__(self) -> str:
        #return f"FE {self.academic_year}"
        return f"AY {self.academic_year}"