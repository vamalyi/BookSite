# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webshopcart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='baskets', verbose_name='Owner'),
        ),
    ]
