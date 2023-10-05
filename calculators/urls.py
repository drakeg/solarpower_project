from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('solar-savings/', views.solar_savings_calculator, name='solar_savings_calculator'),
]