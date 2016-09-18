# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopcart', '0003_auto_20160303_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincart',
            name='count',
            field=models.PositiveIntegerField(),
        ),
    ]
