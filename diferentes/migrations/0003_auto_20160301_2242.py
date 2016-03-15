# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-01 21:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diferentes', '0002_userstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstatus',
            name='id',
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]