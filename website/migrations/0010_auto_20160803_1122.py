# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-03 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20160616_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='news_description',
            field=models.CharField(blank=True, help_text='news description', max_length=255, verbose_name='Description for news'),
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='news_keywords',
            field=models.CharField(blank=True, help_text='news keys', max_length=255, verbose_name='Keywords for news'),
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='news_title',
            field=models.CharField(blank=True, help_text='news title', max_length=255, verbose_name='Title for news'),
        ),
    ]
