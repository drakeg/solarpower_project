# blog/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import BlogPostForm
from .models import BlogPost


def generate_summary(article_text, sentences_count):
    """Return a lightweight sentence summary without external tokenizer data."""
    sentences = []
    current = []
    for character in article_text.strip():
        current.append(character)
        if character in '.!?':
            sentence = ''.join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []
            if len(sentences) == sentences_count:
                break

    if current and len(sentences) < sentences_count:
        sentences.append(''.join(current).strip())

    return ' '.join(sentences)


@require_GET
def home(request):
    active_page = 'blog'
    blog_posts = BlogPost.objects.all().order_by('-date_published')
    paginator = Paginator(blog_posts, 10)
    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)
    for post in blog_posts:
        post.summary = generate_summary(post.content, sentences_count=2)
        post.keywords_list = post.keywords.split(', ') if post.keywords else []
    return render(
        request,
        'blog/blog_list.html',
        {'blog_posts': blog_posts, 'active_page': active_page},
    )


@require_GET
def blog_detail(request, pk):
    active_page = 'blog'
    blog_post = get_object_or_404(BlogPost, pk=pk)
    keywords = [
        keyword.strip()
        for keyword in (blog_post.keywords or '').split(',')
        if keyword.strip()
    ]
    return render(
        request,
        'blog/blog_detail.html',
        {
            'blog_post': blog_post,
            'keywords': keywords,
            'active_page': active_page,
        },
    )


def _can_manage_post(user, blog_post):
    return user.is_authenticated and (user == blog_post.author or user.is_staff)


@login_required
@require_http_methods(['GET', 'POST'])
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


@login_required
@require_http_methods(['GET', 'POST'])
def edit_blog_post(request, pk):
    active_page = 'blog'
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if not _can_manage_post(request.user, blog_post):
        raise PermissionDenied

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm(instance=blog_post)

    return render(
        request,
        'blog/blog_post_form.html',
        {
            'form': form,
            'blog_post': blog_post,
            'active_page': active_page,
        },
    )


@login_required
@require_http_methods(['GET', 'POST'])
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if not _can_manage_post(request.user, blog_post):
        raise PermissionDenied

    if request.method == 'POST':
        blog_post.delete()
        return redirect('blog:home')

    return render(
        request,
        'blog/blog_post_confirm_delete.html',
        {'blog_post': blog_post},
    )
