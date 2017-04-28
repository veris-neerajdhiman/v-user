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
import requests

# Django
from django.conf import settings
from django.contrib.auth import get_user_model

# rest-framework
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# local

# own app
from accounts import serializers, policy

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Note : username Cannot be updated from here.
    """
    model = User
    queryset = model.objects.all()
    # TODO : remove AllowAny permission with proper permission class
    # TODO : User Self permission are not handled via AM server, handle them using AM
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

    def create(self, request):
        """

        :param request:
        :return:
        """
        # ToDo: juggad to avoid password in response.Fix It with some permanent solution.

        original_response = super(UserViewSet, self).create(request)
        user = User.objects.get(uuid=original_response.data.get('uuid'))
        response = serializers.UserSerializer(instance=user)
        return Response(response.data, status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.GenericViewSet):
    """
    We'll keep the LoginView simple for now.
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def user_login(self, request):
        """
        :param request: Django request
        :return:
        """
        # Will only match user name password for now and return user unique uuid in place of token
        # because right ow not sure how we will do authentication.

        # ToDo : Replace login process with some valid Login Mechanism
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=serializer.data.get('username'))
            if user.check_password(serializer.data.get('password')):
                return Response({'token': user.uuid}, status=status.HTTP_200_OK)
        except:
            pass
        return Response(status=status.HTTP_401_UNAUTHORIZED)

