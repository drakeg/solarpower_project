from django.forms import formset_factory
from django.shortcuts import render

from .forms import LoadEstimatorForm, SolarSavingsForm, SolarSystemSizingForm
from .utilities import calculate_daily_load, calculate_savings, calculate_system_size


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


def load_estimator(request):
    active_page = 'calculators'
    load_result = None

    if request.method == 'POST':
        form = LoadEstimatorForm(request.POST)
        if form.is_valid():
            load_result = calculate_daily_load(form.cleaned_data)
    else:
        form = LoadEstimatorForm()

    return render(request, 'calculators/load_estimator.html', {
        'form': form,
        'load_result': load_result,
        'active_page': active_page,
    })


def load_worksheet(request):
    active_page = 'calculators'
    LoadFormSet = formset_factory(LoadEstimatorForm, extra=5, max_num=20)
    total_daily_wh = None
    load_results = []

    if request.method == 'POST':
        formset = LoadFormSet(request.POST)
        if formset.is_valid():
            total_daily_wh = 0
            for form in formset:
                if not form.cleaned_data:
                    continue
                result = calculate_daily_load(form.cleaned_data)
                load_results.append({
                    'name': form.cleaned_data['appliance_name'],
                    **result,
                })
                total_daily_wh += result['daily_wh']
    else:
        formset = LoadFormSet()

    return render(request, 'calculators/load_worksheet.html', {
        'formset': formset,
        'load_results': load_results,
        'total_daily_wh': total_daily_wh,
        'active_page': active_page,
    })
