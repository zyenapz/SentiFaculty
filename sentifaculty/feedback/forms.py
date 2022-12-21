from django import forms
from .models import Student, Section, Strand


class FeedbackStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_ID', 'email']


class FeedbackSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_ID']


class FeedbackStrandForm(forms.ModelForm):
    class Meta:
        model = Strand
        fields = ['strand_name']
