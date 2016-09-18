# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import webshop.models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0004_auto_20160226_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(related_name='products', default=webshop.models.get_default_manufacturer, verbose_name='Manufacturer of product', to='webshop.Manufacturer'),
        ),
    ]
