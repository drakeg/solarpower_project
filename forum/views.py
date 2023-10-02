# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Response, Category
from .forms import ThreadForm, ResponseForm
from django.core.paginator import Paginator

@login_required
def thread_list(request):
    active_page = 'forum'
    categories = Category.objects.all()
    categories_and_threads = []

    for category in categories:
        threads = Thread.objects.filter(category=category)
        categories_and_threads.append((category, threads))

    context = {
        'categories_and_threads': categories_and_threads,
        'active_page': active_page
    }

    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', context)

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum:view_thread', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})

@login_required
def create_response(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            category = thread.category
            response_content = request.POST['content']
            author = request.user
            response = Response(thread=thread, author=author, content=response_content, category=category)
            response.save()
            return redirect('forum:view_thread', thread_id=thread_id)
    else:
        form = ResponseForm()

    return render(request, 'forum/view_thread.html', {'thread': thread, 'response_form': form})

@login_required
def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = thread
            post.save()
            return redirect('view_thread', thread_id)
    else:
        form = ResponseForm()
    return render(request, 'forum/view_thread.html', {'thread': thread, 'form': form})