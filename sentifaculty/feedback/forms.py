from django.forms import ModelForm 
from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import Teacher
from .models import Feedback, Evaluatee

class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = ['comment', 'actual_sentiment']
        widgets = {
            'actual_sentiment': forms.RadioSelect()
        }

class SelectEvaluateeForm(forms.Form):
    # TODO add a way to filter evaluatees based on if they are taken by a Student
    teacher = forms.ModelChoiceField(queryset=Evaluatee.objects.all())

    def __init__(self, *args, **kwargs):
        super(SelectEvaluateeForm, self).__init__(*args, **kwargs)

    #     self.fields['teacher'].label_from_instance = self.label_from_instance

    # @staticmethod
    # def label_from_instance(obj):
    #     fname = obj.user.first_name
    #     lname = obj.user.last_name
    #     return f"{fname} {lname}"
