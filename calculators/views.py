from django.shortcuts import render

from .forms import SolarSavingsForm
from .utilities import calculate_savings


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
