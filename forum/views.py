# forum/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ResponseForm, ThreadForm
from .models import Category, Response, Thread


def thread_list(request):
    active_page = 'forum'
    categories_and_threads = [
        (category, Thread.objects.filter(category=category))
        for category in Category.objects.all()
    ]
    context = {
        'categories_and_threads': categories_and_threads,
        'active_page': active_page,
    }
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
    return render(
        request,
        'forum/create_thread.html',
        {'form': form, 'active_page': active_page},
    )


@login_required
def create_response(request, thread_id):
    active_page = 'forum'
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            Response.objects.create(
                content=form.cleaned_data['content'],
                author=request.user,
                thread=thread,
            )
            return redirect('forum:view_thread', thread_id=thread_id)
    else:
        form = ResponseForm()
    return render(
        request,
        'forum/view_thread.html',
        {
            'thread': thread,
            'responses': Response.objects.filter(thread=thread).order_by('-created_at'),
            'form': form,
            'active_page': active_page,
        },
    )


def view_thread(request, thread_id):
    active_page = 'forum'
    thread = get_object_or_404(Thread, pk=thread_id)
    responses = Response.objects.filter(thread=thread).order_by('-created_at')

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            Response.objects.create(
                content=form.cleaned_data['content'],
                thread=thread,
                author=request.user,
            )
            return redirect('forum:view_thread', thread_id=thread.id)
    else:
        form = ResponseForm()

    return render(
        request,
        'forum/view_thread.html',
        {
            'thread': thread,
            'responses': responses,
            'form': form,
            'active_page': active_page,
        },
    )
