# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Response, Category
from .forms import ThreadForm, ResponseForm
from django.core.paginator import Paginator

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
    active_page = 'forum'
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum:view_thread', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form, 'active_page': active_page})

@login_required
def create_response(request, thread_id):
    active_page = 'forum'
    # Fetch the original thread
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            # Create a new response and set its category to the same as the original thread
            response = Response(
                content=form.cleaned_data['content'],
                author=request.user,
                thread=thread,
                category=thread.category  # Set response's category to the thread's category
            )
            response.save()

            # Redirect to the thread detail page or any other appropriate page
            return redirect('forum:view_thread', thread_id=thread_id)
    else:
        form = ResponseForm()

    return render(request, 'forum/response_form.html', {'form': form, 'active_page': active_page})

def view_thread(request, thread_id):
    active_page='forum'
    thread = get_object_or_404(Thread, pk=thread_id)
    responses = Response.objects.filter(thread=thread).order_by('-created_at')
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            # Save the response and associate it with the thread
            new_response = Response(
                content=form.cleaned_data['content'],
                thread=thread,
                author=request.user
            )
            new_response.save()
            return redirect('forum:view_thread', thread_id=thread.id)

    else:
        form = ResponseForm()

    return render(request, 'forum/view_thread.html', {'thread': thread, 'responses': responses, 'form': form, 'active_page': active_page})