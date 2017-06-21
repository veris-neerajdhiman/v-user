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
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# local

# own app

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are fetch/Update an User.
       Since Email cannot Be updated from Here
    """
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'name', 'email', 'avatar', 'avatar_thumbnail')


class UserCreateSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are creating an User.
    """
    uuid = serializers.UUIDField(read_only=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.filter(is_active=True))]
                                   )
    avatar=serializers.ImageField(required=False)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'name', 'password', 'email', 'avatar', 'avatar_thumbnail', )

    def create(self, validated_data):
        """

        :param validated_data: Serializer validated data
        :return: user object
        """
        password = validated_data.pop('password')

        # catch exception for Integrity error (means user with same email already exists)
        # is user is de-active (is_active=False), then make him active (is_active=true)
        # user is de-active most probably because he was added member as first.
        # so we can make him active

        # ToDo : Handle this member/user with same email using some more convenient way.
        # ToDo : Once Verification notifications are On then we can handle this in some other way

        try:
            user = super(UserCreateSerializer, self).create(validated_data)
        except IntegrityError:
            user = User.objects.get(email=validated_data.get('email'))

            if user.is_active is False:
                user.is_active = True

        user.set_password(password)
        user.save()
        return user


class ShadowUserCreateSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are creating a shadow User.
    """
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(required=True)
    avatar=serializers.ImageField(required=False)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'name', 'email', 'avatar', 'avatar_thumbnail', 'is_active', )

    def create(self, validated_data):
        """Here we check wether already an user exists or not, If not then create else return same user instance.

        :param validated_data: serializer valid data
        :return: user instance
        """
        # if email field violates unique Rule , db will raise IntegrityError and we will catch this error return
        # existing user instance.

        try:
            return super(ShadowUserCreateSerializer, self).create(validated_data)
        except IntegrityError:
            return User.objects.get(email=validated_data.get('email'))


class LoginSerializer(serializers.Serializer):
    """

    """
    email = serializers.CharField(required=True)

    # TODO create a password field to be used
    password = serializers.CharField(required=True)
