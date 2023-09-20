# admin.py in the blog app
from django.contrib import admin
from .models import BlogPost

admin.site.register(BlogPost)