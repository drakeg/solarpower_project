from django.shortcuts import render

from .forms import SolarSavingsForm, SolarSystemSizingForm
from .utilities import calculate_savings, calculate_system_size


def solar_savings_calculator(request):
    active_page = 'calculators'
    savings_breakdown = None
    if request.method == 'POST':
        form = SolarSavingsForm(request.POST)
        if form.is_valid():
            savings_breakdown = calculate_savings(form.cleaned_data)
    else:
        form = SolarSavingsForm()

    return render(request, 'calculators/solar_savings_calculator.html', {
        'form': form,
        'savings_breakdown': savings_breakdown,
        'active_page': active_page
    })


def solar_system_sizing_calculator(request):
    active_page = 'calculators'
    sizing_result = None

    if request.method == 'POST':
        form = SolarSystemSizingForm(request.POST)
        if form.is_valid():
            sizing_result = calculate_system_size(form.cleaned_data)
    else:
        form = SolarSystemSizingForm()

    return render(request, 'calculators/solar_system_sizing.html', {
        'form': form,
        'sizing_result': sizing_result,
        'active_page': active_page,
    })
