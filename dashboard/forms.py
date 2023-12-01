from django import forms
from django.contrib.auth.forms import UserCreationForm
from activityTracker.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'nom', 'prenom', 'dateDeNaissance', 'poids', 'taille')
