# solarpower/views.py
import nltk
from nltk.tokenize import sent_tokenize
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm  # We'll create this form shortly
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

nltk.download('punkt')  # Download the NLTK data for tokenization

def generate_summary(article_text, sentences_count):
    sentences = sent_tokenize(article_text)

    first_two_sentences = ' '.join(sentences[:sentences_count])
    return first_two_sentences

def home(request):
    # Query and customize the blog posts you want to display
    active_page = 'blog'
    blog_posts = BlogPost.objects.all().order_by('-date_published') # Example: Display the latest 5 blog posts
    paginator = Paginator(blog_posts, 10)
    for post in blog_posts:
        post.summary = generate_summary(post.content, sentences_count=2)
        if post.keywords:
            post.keywords_list = post.keywords.split(', ')  # Split keywords into a list
        else:
            post.keywords_list = []  # Handle cases where no keywords are provided
    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)
    return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts, 'active_page': active_page})

def blog_detail(request, pk):
    active_page = 'blog'
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog_post': blog_post, 'active_page': active_page})

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
    return render(request, 'blog/blog_post_form.html', {'form': form, 'active_page': active_page})