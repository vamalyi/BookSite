# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0011_auto_20160314_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='template',
            field=models.ForeignKey(null=True, to='weblayout.Template', blank=True),
        ),
    ]
