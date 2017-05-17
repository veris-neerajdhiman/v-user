#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.admin
~~~~~~~~~~~~~~

- This file contains the admin models of accounts.
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# local

# own app
from accounts.forms import UserCreationForm, AdminUserChangeForm


User = get_user_model()

USERNAME_FIELD = User.USERNAME_FIELD

REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)

BASE_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password',),
})

PROFILE_FIELDS = (_('Profile'), {
    'fields': ('name', 'uuid', 'avatar'),
})

PERMISSION_FIELDS = (_('Permissions'), {
    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
})

DATE_FIELDS = (_('Important dates'), {
    'fields': ('last_login', 'date_joined',),
})


class UserAdmin(DjangoUserAdmin):
    """

    """
    add_form_template = None
    add_form = UserCreationForm
    form = AdminUserChangeForm
    list_per_page = 1000
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', USERNAME_FIELD, 'name', 'uuid', 'avatar_thumbnail', 'is_active', )
    list_display_links = (USERNAME_FIELD, 'uuid',)
    search_fields = ('uuid', USERNAME_FIELD, 'name', )
    fieldsets = (
        BASE_FIELDS,
        PROFILE_FIELDS,
        PERMISSION_FIELDS,
        DATE_FIELDS,
    )
    list_filter = ('is_superuser', 'is_staff', 'is_active',)
    add_fieldsets = (
        (None, {
            'fields': REQUIRED_FIELDS + (
                'password1',
                'password2',
            ),
        }),
    )
    ordering = None
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('uuid', 'last_login', 'date_joined')

    def avatar_thumbnail(self, obj):
        """

        :param obj: user instance
        :return: user avatar thumbanil
        """
        return '<img width="36" height="36" src="%s"/>' % obj.avatar_thumbnail.url if bool(obj.avatar_thumbnail) else ''

    avatar_thumbnail.allow_tags = True

admin.site.register(User, UserAdmin)
