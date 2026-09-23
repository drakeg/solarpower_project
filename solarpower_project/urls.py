"""URL configuration for the SolarPower project."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from solarpower import views as solarpower_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', 'blog')),
    path('user_profile/', solarpower_views.user_profile, name='user_profile'),
    path('register/', solarpower_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forum/', include('forum.urls', 'forum')),
    path('calculators/', include('calculators.urls', 'calculators')),
]
