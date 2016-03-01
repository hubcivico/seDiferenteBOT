# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-01 20:42
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='test', max_length=765, unique=True),
            preserve_default=False,
        ),
    ]
