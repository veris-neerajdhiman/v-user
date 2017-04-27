#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.policy
~~~~~~~~~~~~~~~~~

- This file contains all conversation between User service and AM server
"""

# future
from __future__ import unicode_literals

# 3rd party
import requests

# Django
from django.conf import settings

# local


# own app


ADD_POLICY_URL = '{0}{1}'.format(getattr(settings, 'AM_SERVER_URL'),
                                      getattr(settings, 'ADD_POLICY_API_PATH'))

VALIDATE_POLICY_URL = '{0}{1}'.format(getattr(settings, 'AM_SERVER_URL'),
                                      getattr(settings, 'VALIDATE_POLICY_API_PATH'))

def add_user_policy_for_organization(user_uuid):
    """
    SAMPLE POST Data :
        {
        "source":"user:2db95648-b5ea-458a-9f07-a9ef51bbca21:",
        "source_permission_set":[
            {
            "target":"vrn:resource:organization:",
            "create": true,
            "read":true,
            "update":true,
            "delete":true
            }]

    }
    """
    permission_set = []

    permissions = getattr(settings, 'DEFAULT_ORGANIZATION_PERMISSION_SET')

    # add target in permission set
    permissions.update({
        'target': 'vrn:resource:{0}:'.format(getattr(settings, 'ORGANIZATION_IDENTIFIER'))
    })

    permission_set.append(permissions)

    data = {
        'source': 'user:{0}:'.format(user_uuid),
        'source_permission_set':permission_set
    }

    rq = requests.post(ADD_POLICY_URL, json=data, verify=True)

    return rq
