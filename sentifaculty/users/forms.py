from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MclUser

class MclUserCreationForm(UserCreationForm):
    class Meta:
        model = MclUser
        fields = ("email", "mcl_id", "first_name", "last_name")

class MclUserChangeForm(UserChangeForm):
    class Meta:
        model = MclUser
        fields = ("email", "mcl_id", "first_name", "last_name")