# models.py in the solarpower app
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields for user profiles (e.g., bio, profile picture, etc.)

# Add more models as needed for calculators, user messages, etc.
