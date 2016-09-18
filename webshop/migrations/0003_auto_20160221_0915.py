# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_auto_20160105_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_medium',
            field=image_cropping.fields.ImageRatioField('image_original', '400x270', help_text=None, free_crop=False, adapt_rotation=False, hide_image_field=False, allow_fullsize=False, verbose_name='cropping medium', size_warning=False),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_small',
            field=image_cropping.fields.ImageRatioField('image_original', '250x160', help_text=None, free_crop=False, adapt_rotation=False, hide_image_field=False, allow_fullsize=False, verbose_name='cropping small', size_warning=False),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='product',
            field=models.ForeignKey(to='webshop.Product', related_name='images'),
        ),
    ]
