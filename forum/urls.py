# forum/urls.py
from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('create_response/<int:thread_id>/',  views.create_response, name='create_response'),
    path('view_thread/<int:thread_id>/', views.view_thread, name='view_thread'),
    path('thread/<int:thread_id>/edit/', views.edit_thread, name='edit_thread'),
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('response/<int:response_id>/edit/', views.edit_response, name='edit_response'),
    path('response/<int:response_id>/delete/', views.delete_response, name='delete_response'),
]
