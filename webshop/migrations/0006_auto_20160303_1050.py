# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0005_product_manufacturer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='product_parameter',
            field=models.ForeignKey(related_name='values', to='webshop.ProductParameter'),
        ),
        migrations.AlterField(
            model_name='productparametervalue',
            name='product',
            field=models.ForeignKey(related_name='parameter_values', to='webshop.Product'),
        ),
        migrations.AlterField(
            model_name='productparametervalue',
            name='product_parameter',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', related_name='parameter_values', to='webshop.ProductParameter'),
        ),
        migrations.AlterField(
            model_name='productparametervalue',
            name='value',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='product_parameter', chained_model_field='product_parameter', related_name='parameter_values', null=True, to='webshop.ProductParameterAvailableValue'),
        ),
    ]
