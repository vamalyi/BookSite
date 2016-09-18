# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('webshop', '0008_product_meta_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True, related_name='categories'),
        ),
        migrations.AddField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Moderators', null=True, related_name='categories'),
        ),
    ]
