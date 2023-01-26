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
        slug = kwargs.pop('slug', None) # Correctly obtains slug from url
        super(SelectEvaluateeForm, self).__init__(*args, **kwargs)

    def is_empty_query(self):
        if not self.query.exists():
            return True
        else:
            return False

    #     self.fields['teacher'].label_from_instance = self.label_from_instance

    # @staticmethod
    # def label_from_instance(obj):
    #     fname = obj.user.first_name
    #     lname = obj.user.last_name
    #     return f"{fname} {lname}"
