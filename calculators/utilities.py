# solar_utils.py

def calculate_savings(input_data):
    current_energy_cost = input_data['current_energy_cost']
    solar_system_cost = input_data['solar_system_cost']
    solar_system_lifetime = input_data['solar_system_lifetime']

    # Calculate annual savings
    annual_savings = current_energy_cost * 12 - (solar_system_cost / solar_system_lifetime / 12)

    # Calculate total savings over the system's lifetime
    total_savings = annual_savings * solar_system_lifetime

    return total_savings