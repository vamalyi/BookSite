# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimageposition',
            name='cropping_large',
            field=image_cropping.fields.ImageRatioField('image_original', '1300x500', help_text=None, free_crop=False, adapt_rotation=False, hide_image_field=False, allow_fullsize=False, verbose_name='cropping large', size_warning=False),
        ),
    ]
