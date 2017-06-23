#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.tests.test_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file includes test-cases of settings which are required for user micro-service

"""

# future
from __future__ import unicode_literals

# third party
import os

# Django
from django.conf import settings
from django.test import TestCase


class SettingsTestCase(TestCase):
    """Settings Test Case

    """

    def setUp(self):
        """

        """
        self.env_settings = ('ORGANIZATION_IDENTIFIER',
                             'RUNTIME_IDENTIFIER',
                             'DEFAULT_ORGANIZATION_PERMISSION_SET',
                             'AM_SERVER_URL',
                             'ADD_POLICY_API_PATH',
                             'VALIDATE_POLICY_API_PATH',
                             )

    def test_environment_variables(self):
        """makes sure settings which are necessary for running Organization micro-service are defined in settings.

        """

        for env_setting in self.env_settings:
            if not getattr(settings, env_setting):
                self.assertFalse('{0} environment settings is defined.'.format(env_setting))

        self.assertTrue('Environment settings test passed.')


class EnvironmentVariableTestCase(TestCase):
    """Environment Variables Test case
    """
    def setUp(self):
        """
        """
        self.env_variables = (
            'DATABASE_NAME_USER',
            'DATABASE_USER',
            'DATABASE_PASSWORD',
            'DATABASE_HOST',
            'DATABASE_PORT',
            'SECRET_KEY',
            'AM_SERVER_URL',
            'ORGANIZATION_IDENTIFIER',
            'VRT_IDENTIFIER',
        )

    def test_env_variables(self):
        """Makes sure necessary env variables are declared.
        """
        for key in self.env_variables:
            try:
                return os.environ[key]
            except KeyError:
                self.assertFalse('{0} environment variable is not defined.'.format(key))