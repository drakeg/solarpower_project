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


class SolarSystemSizingForm(forms.Form):
    daily_energy_use = forms.DecimalField(
        label='Daily Energy Use (Wh)',
        min_value=1,
        help_text='Total watt-hours you expect to use in a typical day.',
    )
    peak_sun_hours = forms.DecimalField(
        label='Peak Sun Hours per Day',
        min_value=0.1,
        help_text='Average equivalent full-sun hours available per day.',
    )
    system_efficiency = forms.DecimalField(
        label='Overall System Efficiency (%)',
        min_value=1,
        max_value=100,
        initial=80,
        help_text='Accounts for wiring, controller, inverter, temperature, and other losses.',
    )
    autonomy_days = forms.DecimalField(
        label='Battery Autonomy (days)',
        min_value=0,
        initial=1,
        help_text='Number of days the battery should support the load without solar input.',
    )
    battery_voltage = forms.DecimalField(
        label='Battery Bank Voltage (V)',
        min_value=1,
        initial=12,
        help_text='Nominal battery-bank voltage, such as 12, 24, or 48 volts.',
    )
    usable_battery_percent = forms.DecimalField(
        label='Usable Battery Capacity (%)',
        min_value=1,
        max_value=100,
        initial=80,
        help_text='Percentage of nominal battery capacity you plan to use.',
    )


class LoadEstimatorForm(forms.Form):
    appliance_name = forms.CharField(
        label='Appliance / Load',
        max_length=100,
        help_text='A descriptive name such as refrigerator, laptop, or lights.',
    )
    watts = forms.DecimalField(
        label='Power (W)',
        min_value=0.1,
        help_text='Running power draw in watts for one device.',
    )
    quantity = forms.IntegerField(
        label='Quantity',
        min_value=1,
        initial=1,
    )
    hours_per_day = forms.DecimalField(
        label='Hours Used per Day',
        min_value=0,
        max_value=24,
        help_text='Average number of hours each device runs per day.',
    )
