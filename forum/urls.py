# forum/urls.py
from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('create_response/<int:thread_id>/',  views.create_response, name='create_response'),
    path('view_thread/<int:thread_id>/', views.view_thread, name='view_thread'),
    path('vote/<int:post_id>/<int:value>/', views.vote, name='vote'),
]
