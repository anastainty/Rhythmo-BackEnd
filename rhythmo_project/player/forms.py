from django import forms
from .models import Track
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'album', 'genre', 'duration', 'file', 'release_date']

    enctype = "multipart/form-data"

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)