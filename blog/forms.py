# blog/forms.py
from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
