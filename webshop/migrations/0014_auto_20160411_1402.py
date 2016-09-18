# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0013_auto_20160315_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
