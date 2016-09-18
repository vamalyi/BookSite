# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import webshopcart.models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0007_deliveryrule_code'),
        ('webshopcart', '0002_productcart_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='delivery',
            field=models.ForeignKey(to='webshop.DeliveryRule', default=webshopcart.models.get_default_delivery, related_name='baskets'),
        ),
        migrations.AlterField(
            model_name='productcart',
            name='description',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='cart',
            field=models.ForeignKey(to='webshopcart.ProductCart', related_name='order_items'),
        ),
    ]
