# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 11:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webshop', '0037_auto_20160617_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTreeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='Name')),
                ('email', models.CharField(blank=True, max_length=256, verbose_name='Email')),
                ('body', models.TextField(verbose_name='Review')),
                ('score',
                 models.PositiveIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0,
                                             verbose_name='Score')),
                ('status',
                 models.SmallIntegerField(choices=[(0, 'Requires moderation'), (1, 'Approved'), (2, 'Rejected')],
                                          default=0, verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent',
                 mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='children', to='webshop.ProductTreeReview',
                                            verbose_name='Parent menu item')),
                ('product',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tree_reviews',
                                   to='webshop.Product', verbose_name='Product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='tree_reviews', to=settings.AUTH_USER_MODEL,
                                           verbose_name='Owner')),
            ],
            options={
                'ordering': ('date_created',),
                'verbose_name': 'Product Review',
                'verbose_name_plural': 'Product Reviews',
            },
        ),
    ]
