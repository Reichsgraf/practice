# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0007_auto_20170624_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='pressure',
            field=models.FloatField(),
        ),
    ]
