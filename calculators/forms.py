from django import forms

class SolarSavingsForm(forms.Form):
    current_energy_cost = forms.DecimalField(
        label='Current Monthly Energy Cost',
        min_value=0,
        help_text='Enter your current monthly energy cost. You can find this information on your recent energy bills.'
    )
    solar_system_cost = forms.DecimalField(
        label='Solar System Cost',
        min_value=0,
        help_text='Enter the total cost of the solar system you are considering.'
    )
    solar_system_lifetime = forms.IntegerField(
        label='Solar System Lifetime (in years)',
        min_value=1,
        help_text='Enter the expected lifetime of the solar system in years.'
    )
