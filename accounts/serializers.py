#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.serializer
~~~~~~~~~~~~~~

- This file contains Accounts app serializers
"""

# future
from __future__ import unicode_literals

# 3rd party

# DRF
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django
from django.db import IntegrityError
from django.contrib.auth import get_user_model

# local

# own app

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are fetch/Update an User.
       Since Email cannot Be updated from Here
    """
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(source='username', read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'email', 'avatar', 'avatar_thumbnail')


class UserCreateSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are creating an User.
    """
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(source='username',
                                   required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'email', 'avatar', 'avatar_thumbnail', )
