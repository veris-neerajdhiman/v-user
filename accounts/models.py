#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.models
~~~~~~~~~~~~~~

- This file contains the Accounts(user) models that will map into DB tables.

"""

# future
from __future__ import unicode_literals

# 3rd party
import os, uuid
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Django
from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# local

# own app


def upload_avatar_to(instance, filename):
    """
    Get unique filename for user's profile picture.
    """
    filename_base, filename_ext = os.path.splitext(filename)
    return 'profile_picture/{0}.{1}'.format(
        instance.uuid,
        filename_ext.lower(),
    )


class UserManager(BaseUserManager):
    """
    Custom manager for django's custom User Model.
    Support custom fields (fields other than django.contrib.auth.models.AbstractBaseUser) update while creating user.
    """
    def create_user(self, password=None, **kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    Support custom fields (fields other than django.contrib.auth.models.AbstractBaseUser) to be stored in db.
    """
    name = models.CharField(
        _('name'),
        max_length=100,
        null=True,
        blank=True,
        help_text=_('Required. 100 characters or fewer.'),
    )
    username = models.CharField(
        _('username'),
        max_length=75,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    uuid = models.UUIDField(
        _('User Unique Identifier'),
        default=uuid.uuid4,
        help_text=_('User uuid, this token will be used to link user in other services.'),
    )
    avatar = models.ImageField(
        _('User Profile Picture'),
        upload_to=upload_avatar_to
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['username', ]

    def __str__(self):
        return '<{uuid}>: {username}'.format(
            uuid=self.uuid,
            username=self.username,
        )

    def get_short_name(self):
        """

        """
        return self.name
