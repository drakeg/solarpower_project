"""solarpower_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from solarpower import views as solarpower_views
from django.contrib.auth import views as auth_views
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', solarpower_views.home, name='home'),
    path('blog/', solarpower_views.blog, name='blog'),
    #path('forum/', solarpower_views.forum, name='forum'),
    path('calculator/', solarpower_views.calculator, name='calculator'),
    path('user_profile/', solarpower_views.user_profile, name='user_profile'),
    path('register/', solarpower_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forum/', include('forum.urls', 'forum')),
]
