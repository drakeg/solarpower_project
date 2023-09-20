# forum/models.py
from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)  # Field to track upvotes
    downvotes = models.PositiveIntegerField(default=0)  # Field to track downvotes


    def __str__(self):
        return f'Response to "{self.thread.title}" by {self.author}'

class Vote(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10)

    def upvote(self):
        if self.vote_type == 'downvote':
            self.vote_type = 'upvote'
            self.save()
            self.response.upvote()
    
    def downvote(self):
        if self.vote_type == 'upvote':
            self.vote_type = 'downvote'
            self.save()
            self.response.downvote()

    def __str__(self):
        return f'{self.user.username} voted {self.vote_type} on {self.response}'