# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 12:14
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.SlugField(max_length=255, verbose_name='URL')),
                ('type', models.CharField(choices=[('NEWS', 'News'), ('ARTICLE', 'Article'), ('OVERVIEW', 'Overview')], default='NEWS', max_length=10, verbose_name='Type')),
                ('main_image', models.ImageField(upload_to='news', verbose_name='Main image')),
                ('main_image_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title of main image')),
                ('main_image_description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description of main image')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Body')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_canonical', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_robots', models.CharField(blank=True, max_length=255, null=True)),
                ('h1', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published')], default='DRAFT', max_length=10, verbose_name='Status')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='Owner of post')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'verbose_name': 'Post',
                'ordering': ['-created_date'],
            },
        ),
    ]