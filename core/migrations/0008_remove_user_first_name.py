# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160301_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
    ]
