# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-23 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_cloud_cloud_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloud',
            name='icon',
            field=models.ImageField(null=True, upload_to='cloudness_icon'),
        ),
    ]