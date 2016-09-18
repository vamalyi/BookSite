# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0012_auto_20160315_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='template',
            field=models.ForeignKey(blank=True, null=True, to='weblayout.Template'),
        ),
    ]
