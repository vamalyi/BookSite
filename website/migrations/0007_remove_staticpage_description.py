# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 07:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20160516_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staticpage',
            name='description',
        ),
    ]
