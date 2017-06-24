# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_auto_20170624_0130'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Manager',
        ),
        migrations.AddField(
            model_name='request',
            name='description',
            field=models.CharField(default='-', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='temp_max',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='temp_min',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='wind_description',
            field=models.CharField(default='-', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='wind_direction',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
