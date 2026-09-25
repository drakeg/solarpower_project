# solar_utils.py


def calculate_savings(input_data):
    current_energy_cost = input_data['current_energy_cost']
    solar_system_cost = input_data['solar_system_cost']
    solar_system_lifetime = input_data['solar_system_lifetime']

    annual_utility_cost = current_energy_cost * 12
    annualized_system_cost = solar_system_cost / solar_system_lifetime
    annual_net_savings = annual_utility_cost - annualized_system_cost
    lifetime_utility_cost = annual_utility_cost * solar_system_lifetime
    lifetime_net_savings = lifetime_utility_cost - solar_system_cost

    return {
        'annual_utility_cost': annual_utility_cost,
        'annualized_system_cost': annualized_system_cost,
        'annual_net_savings': annual_net_savings,
        'lifetime_utility_cost': lifetime_utility_cost,
        'lifetime_net_savings': lifetime_net_savings,
    }


def calculate_system_size(input_data):
    daily_energy_use = input_data['daily_energy_use']
    peak_sun_hours = input_data['peak_sun_hours']
    efficiency = input_data['system_efficiency'] / 100
    autonomy_days = input_data['autonomy_days']
    battery_voltage = input_data['battery_voltage']
    usable_battery_fraction = input_data['usable_battery_percent'] / 100

    required_array_watts = daily_energy_use / peak_sun_hours / efficiency
    required_usable_battery_wh = daily_energy_use * autonomy_days
    required_nominal_battery_wh = (
        required_usable_battery_wh / usable_battery_fraction
    )
    required_battery_ah = required_nominal_battery_wh / battery_voltage

    return {
        'required_array_watts': required_array_watts,
        'required_usable_battery_wh': required_usable_battery_wh,
        'required_nominal_battery_wh': required_nominal_battery_wh,
        'required_battery_ah': required_battery_ah,
    }
