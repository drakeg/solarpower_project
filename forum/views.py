# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Response, Vote
from .forms import ThreadForm, ResponseForm

@login_required
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum:thread_list')
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})

@login_required
def create_response(request, thread_id):
    thread = Thread.objects.get(pk=thread_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.thread = thread  # Associate the response with the thread
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

@login_required
def vote(request, response_id, value):
    response = get_object_or_404(Response, pk=response_id)
    user = request.user

    try:
        vote = Vote.objects.get(response=response, voter=user)
        if vote.value != value:
            vote.value = value
            vote.save()
    except Vote.DoesNotExist:
        vote = Vote(response=response, voter=user, value=value)
        vote.save()

    return redirect('view_thread', thread_id=response.thread.id)
