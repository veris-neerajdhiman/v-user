# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-05 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170419_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=1, help_text='Required. 100 characters or fewer.', max_length=100, verbose_name='name'),
            preserve_default=False,
        ),
    ]