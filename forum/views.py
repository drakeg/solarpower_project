# forum/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
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
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
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


def _can_manage_thread(user, thread):
    return user.is_authenticated and (user == thread.author or user.is_staff)


@login_required
def edit_thread(request, thread_id):
    active_page = 'forum'
    thread = get_object_or_404(Thread, pk=thread_id)
    if not _can_manage_thread(request.user, thread):
        raise PermissionDenied

    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum:view_thread', thread_id=thread.id)
    else:
        form = ThreadForm(instance=thread)

    return render(
        request,
        'forum/edit_thread.html',
        {'form': form, 'thread': thread, 'active_page': active_page},
    )


@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if not _can_manage_thread(request.user, thread):
        raise PermissionDenied

    if request.method == 'POST':
        thread.delete()
        return redirect('forum:thread_list')

    return render(request, 'forum/delete_thread.html', {'thread': thread})


def _can_manage_response(user, response):
    return user.is_authenticated and (user == response.author or user.is_staff)


@login_required
def edit_response(request, response_id):
    active_page = 'forum'
    response = get_object_or_404(Response, pk=response_id)
    if not _can_manage_response(request.user, response):
        raise PermissionDenied

    if request.method == 'POST':
        form = ResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('forum:view_thread', thread_id=response.thread_id)
    else:
        form = ResponseForm(instance=response)

    return render(
        request,
        'forum/edit_response.html',
        {'form': form, 'response': response, 'active_page': active_page},
    )


@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, pk=response_id)
    if not _can_manage_response(request.user, response):
        raise PermissionDenied

    thread_id = response.thread_id
    if request.method == 'POST':
        response.delete()
        return redirect('forum:view_thread', thread_id=thread_id)

    return render(request, 'forum/delete_response.html', {'response': response})
