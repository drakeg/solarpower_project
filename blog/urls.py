# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('new/', views.create_blog_post, name='create_blog_post'),
]
