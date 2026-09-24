import importlib
import os
from unittest.mock import patch

from django.test import SimpleTestCase

import solarpower_project.settings as project_settings


class EnvironmentSettingsTests(SimpleTestCase):
    def reload_settings(self, environment):
        with patch.dict(os.environ, environment, clear=True):
            return importlib.reload(project_settings)

    def tearDown(self):
        importlib.reload(project_settings)
        super().tearDown()

    def test_debug_defaults_to_false(self):
        settings = self.reload_settings({'SECRET_KEY': 'test-secret'})

        self.assertFalse(settings.DEBUG)

    def test_debug_accepts_explicit_true_value(self):
        settings = self.reload_settings(
            {'SECRET_KEY': 'test-secret', 'DEBUG': 'true'},
        )

        self.assertTrue(settings.DEBUG)

    def test_allowed_hosts_are_parsed_from_environment(self):
        settings = self.reload_settings(
            {
                'SECRET_KEY': 'test-secret',
                'ALLOWED_HOSTS': 'localhost, 127.0.0.1,solar.example.com',
            },
        )

        self.assertEqual(
            settings.ALLOWED_HOSTS,
            ['localhost', '127.0.0.1', 'solar.example.com'],
        )

    def test_https_security_defaults_remain_local_development_safe(self):
        settings = self.reload_settings({'SECRET_KEY': 'test-secret'})

        self.assertFalse(settings.SECURE_SSL_REDIRECT)
        self.assertFalse(settings.SESSION_COOKIE_SECURE)
        self.assertFalse(settings.CSRF_COOKIE_SECURE)
        self.assertEqual(settings.SECURE_HSTS_SECONDS, 0)

    def test_https_security_can_be_enabled_for_production(self):
        settings = self.reload_settings(
            {
                'SECRET_KEY': 'test-secret',
                'SECURE_SSL_REDIRECT': 'true',
                'SESSION_COOKIE_SECURE': 'true',
                'CSRF_COOKIE_SECURE': 'true',
                'SECURE_HSTS_SECONDS': '31536000',
            },
        )

        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)
        self.assertEqual(settings.SECURE_HSTS_SECONDS, 31536000)
        self.assertTrue(settings.SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertTrue(settings.SECURE_HSTS_PRELOAD)

    def test_missing_secret_key_fails_fast(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'SECRET_KEY'):
                importlib.reload(project_settings)
