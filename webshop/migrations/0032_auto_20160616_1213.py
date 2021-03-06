# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 09:13
from __future__ import unicode_literals

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0031_auto_20160613_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(blank=True, max_length=255, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='bookseries',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=core.utils.image_directory_path, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=core.utils.image_directory_path, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='image_original',
            field=models.ImageField(upload_to=core.utils.image_directory_path, verbose_name='Original image'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='First image of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Second image of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='specialproposition',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.image_directory_path, verbose_name='Image of special proposition'),
        ),
    ]
