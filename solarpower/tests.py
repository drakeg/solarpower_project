from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountViewTests(TestCase):
    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'new-user',
                'password1': 'A-strong-test-password-123',
                'password2': 'A-strong-test-password-123',
            },
        )

        self.assertRedirects(response, reverse('user_profile'))
        self.assertTrue(get_user_model().objects.filter(username='new-user').exists())
        profile = self.client.get(reverse('user_profile'))
        self.assertEqual(profile.status_code, 200)
        self.assertTrue(profile.context['user'].is_authenticated)

    def test_invalid_registration_renders_errors(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'new-user',
                'password1': 'different-password-123',
                'password2': 'does-not-match-456',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(get_user_model().objects.filter(username='new-user').exists())

    def test_profile_route_renders(self):
        response = self.client.get(reverse('user_profile'))

        self.assertEqual(response.status_code, 200)


class CoreNavigationTests(TestCase):
    def test_primary_routes_are_available(self):
        route_names = (
            'blog:home',
            'forum:thread_list',
            'calculators:solar_savings_calculator',
            'register',
            'login',
        )

        for route_name in route_names:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)


class SharedLayoutTests(TestCase):
    def test_shared_navigation_has_no_placeholder_links(self):
        response = self.client.get(reverse('blog:home'))

        self.assertNotContains(response, 'href="#"')

    def test_shared_navigation_uses_unique_dropdown_ids(self):
        response = self.client.get(reverse('blog:home'))
        content = response.content.decode()

        self.assertEqual(content.count('id="calculatorsDropdown"'), 1)
        self.assertEqual(content.count('id="guestDropdown"'), 1)
        self.assertNotIn('id="navbarDropdown"', content)

    def test_shared_layout_does_not_advertise_bootstrap_example_canonical(self):
        response = self.client.get(reverse('blog:home'))

        self.assertNotContains(response, 'getbootstrap.com/docs/5.3/examples/blog')

    def test_footer_uses_current_year(self):
        response = self.client.get(reverse('blog:home'))

        self.assertContains(response, 'Solar Education Site. All rights reserved.')
        self.assertNotContains(response, '&copy; 2023', html=False)
