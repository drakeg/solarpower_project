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

    def test_profile_requires_login(self):
        response = self.client.get(reverse('user_profile'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('user_profile')}",
        )

    def test_profile_route_renders_for_authenticated_user(self):
        user = get_user_model().objects.create_user(
            username='profile-user',
            password='test-password',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('user_profile'))

        self.assertEqual(response.status_code, 200)

    def test_registration_rejects_unsupported_methods(self):
        response = self.client.put(reverse('register'))

        self.assertEqual(response.status_code, 405)


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
    def test_shared_navigation_omits_nonfunctional_placeholder_controls(self):
        response = self.client.get(reverse('blog:home'))

        for label in ('Contact', 'About', 'Messages', 'Search'):
            with self.subTest(label=label):
                self.assertNotContains(response, f'>{label}<')

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


class AccountTemplateTests(TestCase):
    def test_registration_page_has_balanced_container_and_visible_actions(self):
        response = self.client.get(reverse('register'))

        self.assertContains(response, '<div class="container my-5">', html=False)
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Cancel')

    def test_login_page_has_visible_actions(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'Login')
        self.assertContains(response, 'Cancel')
