from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .utilities import calculate_daily_load, calculate_savings, calculate_system_size


class SolarSavingsCalculatorTests(TestCase):
    def test_get_displays_calculator_form(self):
        response = self.client.get(reverse('calculators:solar_savings_calculator'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['savings_breakdown'])
        self.assertEqual(response.context['active_page'], 'calculators')

    def test_valid_post_calculates_savings(self):
        response = self.client.post(
            reverse('calculators:solar_savings_calculator'),
            {
                'current_energy_cost': '200.00',
                'solar_system_cost': '24000.00',
                'solar_system_lifetime': '20',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['savings_breakdown']['annual_utility_cost'], Decimal('2400.00'))
        self.assertEqual(response.context['savings_breakdown']['annualized_system_cost'], Decimal('1200.00'))
        self.assertEqual(response.context['savings_breakdown']['annual_net_savings'], Decimal('1200.00'))
        self.assertEqual(response.context['savings_breakdown']['lifetime_utility_cost'], Decimal('48000.00'))
        self.assertEqual(response.context['savings_breakdown']['lifetime_net_savings'], Decimal('24000.00'))

    def test_invalid_post_does_not_reference_unassigned_result(self):
        response = self.client.post(
            reverse('calculators:solar_savings_calculator'),
            {
                'current_energy_cost': '',
                'solar_system_cost': '24000.00',
                'solar_system_lifetime': '20',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNone(response.context['savings_breakdown'])

    def test_negative_costs_and_zero_lifetime_are_rejected(self):
        response = self.client.post(
            reverse('calculators:solar_savings_calculator'),
            {
                'current_energy_cost': '-1.00',
                'solar_system_cost': '-24000.00',
                'solar_system_lifetime': '0',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNone(response.context['savings_breakdown'])


class CalculateSavingsTests(TestCase):
    def test_calculate_savings_uses_decimal_inputs(self):
        result = calculate_savings(
            {
                'current_energy_cost': Decimal('200.00'),
                'solar_system_cost': Decimal('24000.00'),
                'solar_system_lifetime': 20,
            },
        )

        self.assertEqual(result['annual_utility_cost'], Decimal('2400.00'))
        self.assertEqual(result['annualized_system_cost'], Decimal('1200.00'))
        self.assertEqual(result['annual_net_savings'], Decimal('1200.00'))
        self.assertEqual(result['lifetime_utility_cost'], Decimal('48000.00'))
        self.assertEqual(result['lifetime_net_savings'], Decimal('24000.00'))


class SolarSystemSizingTests(TestCase):
    def test_get_displays_system_sizing_form(self):
        response = self.client.get(
            reverse('calculators:solar_system_sizing_calculator'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['sizing_result'])
        self.assertEqual(response.context['active_page'], 'calculators')

    def test_valid_post_calculates_array_and_battery_requirements(self):
        response = self.client.post(
            reverse('calculators:solar_system_sizing_calculator'),
            {
                'daily_energy_use': '2400',
                'peak_sun_hours': '5',
                'system_efficiency': '80',
                'autonomy_days': '1',
                'battery_voltage': '12',
                'usable_battery_percent': '80',
            },
        )

        result = response.context['sizing_result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['required_array_watts'], Decimal('600'))
        self.assertEqual(result['required_usable_battery_wh'], Decimal('2400'))
        self.assertEqual(result['required_nominal_battery_wh'], Decimal('3000'))
        self.assertEqual(result['required_battery_ah'], Decimal('250'))

    def test_invalid_sizing_inputs_do_not_calculate(self):
        response = self.client.post(
            reverse('calculators:solar_system_sizing_calculator'),
            {
                'daily_energy_use': '0',
                'peak_sun_hours': '0',
                'system_efficiency': '0',
                'autonomy_days': '-1',
                'battery_voltage': '0',
                'usable_battery_percent': '0',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNone(response.context['sizing_result'])


class CalculateSystemSizeTests(TestCase):
    def test_calculate_system_size_uses_efficiency_and_usable_capacity(self):
        result = calculate_system_size(
            {
                'daily_energy_use': Decimal('2400'),
                'peak_sun_hours': Decimal('5'),
                'system_efficiency': Decimal('80'),
                'autonomy_days': Decimal('1'),
                'battery_voltage': Decimal('12'),
                'usable_battery_percent': Decimal('80'),
            },
        )

        self.assertEqual(result['required_array_watts'], Decimal('600'))
        self.assertEqual(result['required_nominal_battery_wh'], Decimal('3000'))
        self.assertEqual(result['required_battery_ah'], Decimal('250'))


class LoadEstimatorTests(TestCase):
    def test_get_displays_load_estimator_form(self):
        response = self.client.get(reverse('calculators:load_estimator'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['load_result'])
        self.assertEqual(response.context['active_page'], 'calculators')

    def test_valid_post_calculates_daily_energy(self):
        response = self.client.post(
            reverse('calculators:load_estimator'),
            {
                'appliance_name': 'Laptop',
                'watts': '65',
                'quantity': '2',
                'hours_per_day': '8',
            },
        )

        result = response.context['load_result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['daily_wh'], Decimal('1040'))
        self.assertEqual(result['daily_kwh'], Decimal('1.04'))

    def test_invalid_load_inputs_do_not_calculate(self):
        response = self.client.post(
            reverse('calculators:load_estimator'),
            {
                'appliance_name': 'Invalid',
                'watts': '0',
                'quantity': '0',
                'hours_per_day': '25',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNone(response.context['load_result'])


class CalculateDailyLoadTests(TestCase):
    def test_calculate_daily_load_accounts_for_quantity_and_runtime(self):
        result = calculate_daily_load(
            {
                'watts': Decimal('65'),
                'quantity': 2,
                'hours_per_day': Decimal('8'),
            },
        )

        self.assertEqual(result['daily_wh'], Decimal('1040'))
        self.assertEqual(result['daily_kwh'], Decimal('1.04'))


class LoadWorksheetTests(TestCase):
    def test_get_displays_multiple_load_rows(self):
        response = self.client.get(reverse('calculators:load_worksheet'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['formset'].forms), 5)
        self.assertIsNone(response.context['total_daily_wh'])

    def test_multiple_loads_are_totaled(self):
        response = self.client.post(
            reverse('calculators:load_worksheet'),
            {
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '20',
                'form-0-appliance_name': 'Laptop',
                'form-0-watts': '65',
                'form-0-quantity': '2',
                'form-0-hours_per_day': '8',
                'form-1-appliance_name': 'Lights',
                'form-1-watts': '10',
                'form-1-quantity': '4',
                'form-1-hours_per_day': '5',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].is_valid())
        self.assertEqual(response.context['total_daily_wh'], Decimal('1240'))
        self.assertEqual(response.context['total_daily_kwh'], Decimal('1.24'))
        self.assertEqual(len(response.context['load_results']), 2)

    def test_blank_rows_are_ignored(self):
        response = self.client.post(
            reverse('calculators:load_worksheet'),
            {
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '20',
                'form-0-appliance_name': 'Fan',
                'form-0-watts': '40',
                'form-0-quantity': '1',
                'form-0-hours_per_day': '6',
                'form-1-appliance_name': '',
                'form-1-watts': '',
                'form-1-quantity': '',
                'form-1-hours_per_day': '',
            },
        )

        self.assertTrue(response.context['formset'].is_valid())
        self.assertEqual(response.context['total_daily_wh'], Decimal('240'))
        self.assertEqual(len(response.context['load_results']), 1)

    def test_partially_filled_row_is_rejected(self):
        response = self.client.post(
            reverse('calculators:load_worksheet'),
            {
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '20',
                'form-0-appliance_name': 'Fan',
                'form-0-watts': '',
                'form-0-quantity': '',
                'form-0-hours_per_day': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['formset'].is_valid())
        self.assertIsNone(response.context['total_daily_wh'])
