# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 09:13
from __future__ import unicode_literals

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0009_auto_20160516_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Image of menu item'),
        ),
    ]
