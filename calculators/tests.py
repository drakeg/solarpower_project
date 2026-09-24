from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .utilities import calculate_savings


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
