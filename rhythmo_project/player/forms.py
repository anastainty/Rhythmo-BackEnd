from django import forms
from .models import Track


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'album', 'genre', 'duration', 'file', 'release_date']

    enctype = "multipart/form-data"