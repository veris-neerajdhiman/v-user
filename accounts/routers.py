#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.routers
~~~~~~~~~~~~~~

- This file contains Accounts router
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.conf.urls import url

# local

# own app
from accounts import views

UUID_REGEX = '[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}'

user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

shadow_user = views.UserViewSet.as_view({
    'post': 'get_or_create_shadow_user'
})

user_memberships = views.UserViewSet.as_view({
    'get': 'get_user_memberships'
})

urlpatterns = [
    url(r'^$',
        user_list,
        name='user-list'),
    url(r'^(?P<uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        user_detail,
        name='user-detail'),
    url(r'^shadow/$',
        shadow_user,
        name='get-or-create-shadow-user'),
    url(r'^(?P<uuid>{uuid})/memberships/$'.format(uuid=UUID_REGEX),
        user_memberships,
        name='get-user-memberships'),
]

