from django import forms


class SubjectSortForm(forms.Form):
    subject = forms.ChoiceField(
        choices=(), label='select subject', widget=forms.Select())

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(SubjectSortForm, self).__init__(*args, **kwargs)
        self.fields['subject'].choices = choices
