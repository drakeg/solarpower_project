# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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

@require_POST
def vote_response(request):
    response_id = request.GET.get('response_id')  # Retrieve response_id from URL parameter
    vote_type = request.GET.get('vote_type')  # Retrieve vote_type from URL parameter

    try:
        response = Response.objects.get(pk=response_id)
        
        # Check if the user has already voted for this response
        existing_vote = Vote.objects.filter(user=request.user, response=response).first()
        
        if existing_vote:
            # Handle existing vote updates (increment/decrement) based on the vote_type
            if vote_type == 'upvote':
                existing_vote.upvote()
            elif vote_type == 'downvote':
                existing_vote.downvote()
        else:
            # Handle new vote creation
            new_vote = Vote(user=request.user, response=response, vote_type=vote_type)
            new_vote.save()
    
        # Send a JsonResponse with the updated upvotes and downvotes counts
        return JsonResponse({'success': True, 'upvotes': response.upvotes, 'downvotes': response.downvotes})
    
    except Response.DoesNotExist:
        return JsonResponse({'success': False, 'error_message': 'Response not found'})