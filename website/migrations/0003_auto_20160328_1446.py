# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20160221_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimageposition',
            name='banner',
            field=models.ForeignKey(to='website.Banner', related_name='banners'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='description',
            field=models.TextField(null=True, max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='template',
            field=models.ForeignKey(to='weblayout.Template', blank=True, null=True),
        ),
    ]
