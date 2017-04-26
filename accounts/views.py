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

    def get_queryset(self):
        """
        Optionally restricts the returned users,
        by filtering against a `is_active` query parameter in the URL.
        """
        queryset = self.queryset

        # filter for active users
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset

    def get_serializer_class(self):
        """For POST method we will use different Serializer

        :return: Serializer Class
        """
        if self.request.method == 'POST':
            return serializers.UserCreateSerializer
        return self.serializer_class

    def get_or_create_shadow_user(self, request):
        """This function is used to get or create shadow user, to be used by Member Service

        :return: user instance
        """
        # ToDo: Limit this API usage by AM server so that only those services can create Shadow User who are entitled to.

        serializer = serializers.ShadowUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user_memberships(self, request):
        """

        :return: User MemberShips list
        """
        pass
