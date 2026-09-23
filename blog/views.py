# blog/views.py
import nltk
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from nltk.tokenize import sent_tokenize

from .forms import BlogPostForm
from .models import BlogPost

nltk.download('punkt')


def generate_summary(article_text, sentences_count):
    sentences = sent_tokenize(article_text)
    return ' '.join(sentences[:sentences_count])


def home(request):
    active_page = 'blog'
    blog_posts = BlogPost.objects.all().order_by('-date_published')
    paginator = Paginator(blog_posts, 10)
    for post in blog_posts:
        post.summary = generate_summary(post.content, sentences_count=2)
        post.keywords_list = post.keywords.split(', ') if post.keywords else []
    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)
    return render(
        request,
        'blog/blog_list.html',
        {'blog_posts': blog_posts, 'active_page': active_page},
    )


def blog_detail(request, pk):
    active_page = 'blog'
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(
        request,
        'blog/blog_detail.html',
        {'blog_post': blog_post, 'active_page': active_page},
    )


@login_required
def create_blog_post(request):
    active_page = 'blog'
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog:blog_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(
        request,
        'blog/blog_post_form.html',
        {'form': form, 'active_page': active_page},
    )
