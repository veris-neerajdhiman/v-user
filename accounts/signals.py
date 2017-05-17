#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.signals
~~~~~~~~~~~~~~~~~~

- This file contains the Accounts app signals
"""

# future
from __future__ import unicode_literals

# 3rd party
import requests

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


@receiver(post_save, sender=User)
def add_user_as_member_in_veris_organization(sender, instance, created=False, **kwargs):
    """Here every new user will be added in Veris Organization

    :param sender: Signal sender
    :param instance: User instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    # FIXME : Move this Veris Organization Signal to workflow asap , this is just a temporary solution thats why

    # hard code token is used.
    if created:
        data = {
            'name': instance.name if instance.name is not None else 'example',
            'email': instance.email,
            'type': 'user',
        }

        # add as Member
        member_server_url = 'http://local.veris.in:8015/'
        member_add_url = 'micro-service/user/{user_uuid}/organization/{org_uuid}/member/'.format(
            user_uuid='43c48028-4992-484a-8aef-7783bc4c5d75',
            org_uuid='8120f31f-e9b8-496b-96b4-a0060b0bc170'
        )

        url = '{0}{1}'.format(member_server_url, member_add_url)

        response = requests.post(url, data=data)

        pass
