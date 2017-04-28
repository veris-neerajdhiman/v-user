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
    # 'get': 'list',
    'post': 'create'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_login = views.LoginViewSet.as_view({
    'post': 'user_login'
})

shadow_user = views.UserViewSet.as_view({
    'post': 'get_or_create_shadow_user'
})


urlpatterns = [
    url(r'^$',
        user_list,
        name='user-list'),
    url(r'^(?P<uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        user_detail,
        name='user-detail'),
    url(r'^login/$'.format(uuid=UUID_REGEX),
        user_login,
        name='user-login'),
    url(r'^shadow/$',
        shadow_user,
        name='get-or-create-shadow-user'),
]

