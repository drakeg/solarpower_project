# solarpower/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm  # We'll create this form shortly
from django.contrib.auth.decorators import login_required

def blog_list(request):
    blog_posts = BlogPost.objects.all().order_by('-date_published')
    return render(request, 'solarpower/blog/blog_list.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'solarpower/blog/blog_detail.html', {'blog_post': blog_post})

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('solarpower:blog_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'solarpower/blog/blog_post_form.html', {'form': form})