# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20160511_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpage',
            name='is_news',
            field=models.BooleanField(default=False, verbose_name='Is news?'),
        ),
    ]
