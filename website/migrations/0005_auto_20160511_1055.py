# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 07:55
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20160411_1402'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalsettings',
            options={'verbose_name': 'Global settings', 'verbose_name_plural': 'Global settings'},
        ),
        migrations.AlterModelOptions(
            name='variable',
            options={'verbose_name': 'Variable', 'verbose_name_plural': 'Variables'},
        ),
        migrations.RemoveField(
            model_name='staticpage',
            name='title',
        ),
        migrations.AddField(
            model_name='staticpage',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='staticpage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title for page'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='banner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='website.Banner', verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='image_large',
            field=models.ImageField(blank=True, null=True, upload_to='image_positions/banners/', verbose_name='Large image'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='image_medium',
            field=models.ImageField(blank=True, null=True, upload_to='image_positions/banners/', verbose_name='Medium image'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='image_original',
            field=models.ImageField(upload_to='image_positions/banners/', verbose_name='Original image'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='image_small',
            field=models.ImageField(blank=True, null=True, upload_to='image_positions/banners/', verbose_name='Small image'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='bannerimageposition',
            name='weight',
            field=models.IntegerField(verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to='galleries_covers/', verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to='galleries_covers/', verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.Gallery', verbose_name='Gallery'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='image_original',
            field=models.ImageField(upload_to='image_positions/galleries/', verbose_name='Original image'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='weight',
            field=models.IntegerField(verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to='static_page/', verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='first_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='First text'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Gallery', verbose_name='Gallery'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='h1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='H1'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='is_news',
            field=models.BooleanField(verbose_name='Is news?'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='meta_canonical',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='meta_robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to='static_page/', verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='second_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Second text'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weblayout.Template', verbose_name='Alternative template'),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='url',
            field=models.CharField(max_length=256, unique=True, verbose_name='URL'),
        ),
    ]
