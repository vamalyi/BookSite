# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0006_auto_20160303_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryrule',
            name='code',
            field=models.CharField(unique=True, max_length=256, null=True),
        ),
    ]
