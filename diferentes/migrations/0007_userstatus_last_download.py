# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diferentes', '0006_userstatus_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='last_download',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]