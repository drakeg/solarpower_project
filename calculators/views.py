from django.shortcuts import render
from .forms import SolarSavingsForm
from .utilities import calculate_savings

def solar_savings_calculator(request):
    active_page = 'calculators'
    if request.method == 'POST':
        form = SolarSavingsForm(request.POST)
        if form.is_valid():
            savings_result = calculate_savings(form.cleaned_data)
    else:
        form = SolarSavingsForm()
        savings_result = None

    return render(request, 'calculators/solar_savings_calculator.html', {
        'form': form,
        'savings_result': savings_result,
        'active_page': active_page
    })