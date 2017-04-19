#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.views
~~~~~~~~~~~~~~

- - This file holds the code for resolving any URL/Router, to resolve any API every request will go through here.
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib.auth import get_user_model

# rest-framework
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# local

# own app
from accounts import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Note : username Cannot be updated from here.
    """
    model = User
    queryset = model.objects.all()
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    lookup_field = 'uuid'

    def get_serializer_class(self):
        """For POST method we will use different Serializer

        :return: Serializer Class
        """
        if self.request.method == 'POST':
            return serializers.UserCreateSerializer
        return self.serializer_class
