# solarpower/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm  # We'll create this form shortly
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def blog_list(request):
    active_page = 'blog'
    blog_posts = BlogPost.objects.all().order_by('-date_published')
    paginator = Paginator(blog_posts, 10)

    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)

    return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    active_page = 'blog'
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog_post': blog_post})

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog:blog_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_post_form.html', {'form': form})