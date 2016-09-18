# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Banners',
                'db_table': 'banners',
                'verbose_name': 'Banner',
            },
        ),
        migrations.CreateModel(
            name='BannerImagePosition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_original', models.ImageField(upload_to='image_positions/banners/')),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('image_medium', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('image_large', models.ImageField(blank=True, null=True, upload_to='image_positions/banners/')),
                ('name', models.CharField(unique=True, max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('banner', models.ForeignKey(to='website.Banner')),
            ],
            options={
                'verbose_name_plural': 'Banner Image Positions',
                'db_table': 'banner_image_positions',
                'verbose_name': 'Banner Image Position',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='galleries_covers/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='galleries_covers/')),
            ],
            options={
                'verbose_name_plural': 'Galleries',
                'db_table': 'galleries',
                'verbose_name': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='GalleryImagePosition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_original', models.ImageField(upload_to='image_positions/galleries/')),
                ('cropping_large', image_cropping.fields.ImageRatioField('image_original', '1200x800', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping large', hide_image_field=False, adapt_rotation=False)),
                ('cropping_medium', image_cropping.fields.ImageRatioField('image_original', '750x230', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping medium', hide_image_field=False, adapt_rotation=False)),
                ('cropping_small', image_cropping.fields.ImageRatioField('image_original', '62x44', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping small', hide_image_field=False, adapt_rotation=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('gallery', models.ForeignKey(to='website.Gallery')),
            ],
            options={
                'verbose_name_plural': 'Gallery Image Positions',
                'db_table': 'gallery_image_positions',
                'verbose_name': 'Gallery Image Position',
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('url', models.CharField(unique=True, max_length=256)),
                ('first_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('second_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('is_news', models.BooleanField()),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='static_page/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='static_page/')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('gallery', models.ForeignKey(to='website.Gallery', blank=True, null=True)),
                ('template', models.ForeignKey(to='weblayout.Template')),
            ],
            options={
                'verbose_name_plural': 'Static Pages',
                'db_table': 'static_pages',
                'verbose_name': 'Static Page',
            },
        ),
    ]
