from django.shortcuts import render
from .models import BlogPost

def post_list(request):
    post = BlogPost.objects.all()
    return render(request, 'blog/post_list.html', {'post': post})
