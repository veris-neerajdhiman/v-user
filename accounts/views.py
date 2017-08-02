#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.views
~~~~~~~~~~~~~~~~

- - This file holds the code for resolving any URL/Router, to resolve any API every request will go through here.
"""

# future
from __future__ import unicode_literals

# 3rd party
from datetime import datetime, timedelta

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# rest-framework
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# local

# own app
from auth.jwt import create_jwt
from accounts import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Note : username Cannot be updated from here.
    """
    model = User
    queryset = model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(queryset, **{'pk': self.request.user.pk})

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

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

    def get_permissions(self):
        """

        :return:
        """
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        return super(UserViewSet, self).get_permissions()

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

    def create(self, request, *args, **kwargs):
        """

        :param request: Django request
        :return:
        """
        serializer_cls = self.get_serializer_class()
        serializer = serializer_cls(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate user json web token
        payload = get_jwt_payload(user)
        token = create_jwt(payload,
                           getattr(settings, 'JWT_PUBLIC_KEY', None),
                           getattr(settings, 'ALGORITHM', 'HS256'))

        response = serializers.UserSerializer(instance=user).data
        response.update({
            'token': token
        })

        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """

        :param request: Django Request
        :return: User detail
        """
        return super(UserViewSet, self).retrieve(request, instance=request.user, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """

        :param request: Django Request
        :return: User detail
        """
        return super(UserViewSet, self).partial_update(request, instance=request.user, *args, **kwargs)


class LoginViewSet(viewsets.GenericViewSet):
    """
    We'll keep the LoginView simple for now.
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny, )

    def user_login(self, request):
        """
        :param request: Django request
        :return: Json web token
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data.get('email'))
            if user.check_password(serializer.data.get('password')):
                payload = get_jwt_payload(user)
                token = create_jwt(payload,
                                   getattr(settings, 'JWT_PUBLIC_KEY', None),
                                   getattr(settings, 'ALGORITHM', 'HS256'))

                response = serializers.UserSerializer(instance=user).data
                response.update({
                    'token': token
                })
                return Response(response, status=status.HTTP_200_OK)
        except:
            pass
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def get_jwt_payload(user):
    """

    :param user: User object
    :return: jwt necessary information
    """
    expiration_time = datetime.utcnow() + timedelta(seconds=getattr(settings, 'TOKEN_EXPIRATION_TIME', 432000))

    return {
        'info': serializers.UserSerializer(instance=user).data,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
        'iss': getattr(settings, 'ISSUER', 'noapp'),
        'aud': getattr(settings, 'AUDIENCE', 'noapp-services')
    }
