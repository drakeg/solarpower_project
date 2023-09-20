from django.contrib import admin
from .models import Thread, Response, Vote

admin.site.register(Thread)
admin.site.register(Response)
admin.site.register(Vote)