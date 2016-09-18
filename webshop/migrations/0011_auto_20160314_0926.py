# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0010_auto_20160314_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(verbose_name='Moderators', to=settings.AUTH_USER_MODEL, blank=True, related_name='categories'),
        ),
    ]
