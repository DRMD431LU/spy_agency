from django import forms
from .models import Hit, Assignment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class HitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ['description', 'target']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
            "user_type"
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
            "user_type"
        )

class CreateAssignForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignee', 'hit', 'status_type']
        labels = {
            "assignee": "Asignar a:",
            "hit": "Hit:",
            "status_type": "Estatus de asignacion:"
        }
