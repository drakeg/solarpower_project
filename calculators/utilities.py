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
