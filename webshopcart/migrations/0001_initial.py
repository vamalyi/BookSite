# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, null=True, max_length=256)),
                ('phone', models.CharField(max_length=256)),
                ('description', models.TextField(max_length=256)),
                ('date_on_add', models.DateTimeField(auto_now_add=True)),
                ('date_on_close', models.DateTimeField(blank=True, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('fixed_sum', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Carts',
                'db_table': 'product_carts',
                'verbose_name': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
                ('cart', models.ForeignKey(to='webshopcart.ProductCart')),
                ('price_correction', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='product', chained_model_field='product', to='webshop.ProductPriceCorrector', blank=True, null=True)),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'verbose_name_plural': 'Products in Carts',
                'db_table': 'products_in_carts',
                'verbose_name': 'Product in Cart',
            },
        ),
    ]
