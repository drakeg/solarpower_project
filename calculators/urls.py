from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('solar-savings/', views.solar_savings_calculator, name='solar_savings_calculator'),
    path('system-sizing/', views.solar_system_sizing_calculator, name='solar_system_sizing_calculator'),
    path('load-estimator/', views.load_estimator, name='load_estimator'),
    path('load-worksheet/', views.load_worksheet, name='load_worksheet'),
]
