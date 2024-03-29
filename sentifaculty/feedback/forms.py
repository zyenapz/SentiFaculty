from django.forms import ModelForm 
from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import Teacher
from .models import Comment, Feedback, Evaluatee

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['evaluatee', 'evaluator', 'comment']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'actual_sentiment']
        widgets = {
            'actual_sentiment': forms.RadioSelect()
        }

class SelectEvaluateeForm(forms.Form):
    # TODO add a way to filter evaluatees based on if they are taken by a Student
    query = Evaluatee.objects.all()
    #query = Evaluatee.objects.filter(teacher__user__first_name="Lolzzzzzz").values()
    
    try:
        ids = [obj.id for obj in query]
    except:
        ids = list()

    # Fields
    evaluatee = forms.ModelChoiceField(queryset=query, widget=forms.RadioSelect(attrs={'class': 'card-input-element d-none'}))

    def __init__(self, *args, **kwargs):
        super(SelectEvaluateeForm, self).__init__(*args, **kwargs)

    # def is_empty_query(self):
    #     print(self.evaluatee.field.queryset.exists())
    #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #     if not self.evaluatee.field.queryset.exists():
    #         return True
    #     else:
    #         return False