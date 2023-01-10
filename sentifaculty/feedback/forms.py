from django.forms import ModelForm 
from django import forms

from users.models import Teacher
from .models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'actual_sentiment']

class SelectTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        super(SelectTeacherForm, self).__init__(*args, **kwargs)

        self.fields['teacher'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        fname = obj.user.first_name
        lname = obj.user.last_name
        return f"{fname} {lname}"
