# admin.py in the blog app
from django.contrib import admin
from .models import BlogPost, ForumPost

admin.site.register(BlogPost)
admin.site.register(ForumPost)
