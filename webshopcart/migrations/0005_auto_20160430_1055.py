# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopcart', '0004_auto_20160411_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcart',
            name='fixed_sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
