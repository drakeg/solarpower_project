from django.contrib import admin
from .models import Thread, Response, Category

admin.site.register(Thread)
admin.site.register(Response)
admin.site.register(Category)