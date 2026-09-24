from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .utilities import calculate_savings


class SolarSavingsCalculatorTests(TestCase):
    def test_get_displays_calculator_form(self):
        response = self.client.get(reverse('calculators:solar_savings_calculator'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['savings_result'])
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
        self.assertEqual(response.context['savings_result'], Decimal('46800.00'))

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
        self.assertIsNone(response.context['savings_result'])


class CalculateSavingsTests(TestCase):
    def test_calculate_savings_uses_decimal_inputs(self):
        result = calculate_savings(
            {
                'current_energy_cost': Decimal('200.00'),
                'solar_system_cost': Decimal('24000.00'),
                'solar_system_lifetime': 20,
            },
        )

        self.assertEqual(result, Decimal('46800.00'))
