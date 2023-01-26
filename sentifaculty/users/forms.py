from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MalayanUser

class MalayanUserCreationForm(UserCreationForm):
    class Meta:
        model = MalayanUser
        fields = ("email", "mcl_id", "first_name", "last_name")

class MalayanUserChangeForm(UserChangeForm):
    class Meta:
        model = MalayanUser
        fields = ("email", "mcl_id", "first_name", "last_name")