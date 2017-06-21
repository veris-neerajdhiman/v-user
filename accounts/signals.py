#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.signals
~~~~~~~~~~~~~~~~~~

- This file contains the Accounts app signals
"""

# future
from __future__ import unicode_literals

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# local

# own app
from accounts import policy

User = get_user_model()


@receiver(post_save, sender=User)
def add_default_policies_for_user_on_am_server(sender, instance, created=False, **kwargs):
    """Here default services for User will be enabled by adding policies on AM server

    :param sender: Signal sender
    :param instance: User instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    if created:
        # Add Policy for Organization
        policy.add_user_policy_for_organization(instance.uuid)
