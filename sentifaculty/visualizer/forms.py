from django import forms

from visualizer.models import FacultyEvaluation


class SubjectSortForm(forms.Form):
    subject = forms.ChoiceField(
        choices=(), label='select subject', widget=forms.Select())

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(SubjectSortForm, self).__init__(*args, **kwargs)
        self.fields['subject'].choices = choices

class FEPeriodForm(forms.Form):
    fe = forms.ModelChoiceField(
        queryset=FacultyEvaluation.objects.all(),
        required=True
    )