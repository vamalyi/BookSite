# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0003_auto_20160221_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Manufacturer name', unique=True)),
                ('slug', models.SlugField(max_length=256, verbose_name='Slug', unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='manufacturer', max_length=255, blank=True, verbose_name='Image', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='productpricecorrector',
            name='product',
            field=models.ForeignKey(related_name='price_correctors', to='webshop.Product'),
        ),
    ]
