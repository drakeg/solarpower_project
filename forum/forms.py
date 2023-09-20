# forum/forms.py
from django import forms
from .models import Thread, Response

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
