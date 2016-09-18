# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefilter',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='specialproposition',
            name='image',
            field=models.ImageField(null=True, upload_to='special_propositions/', blank=True),
        ),
    ]
