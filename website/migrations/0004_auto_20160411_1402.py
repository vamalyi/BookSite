# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20160328_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('company_name', models.CharField(verbose_name='Company name', max_length=255)),
                ('emails', models.TextField(verbose_name='Emails')),
                ('product_title', models.CharField(help_text='product title', default='купить <category> <product> в Киеве недорого - <company>', verbose_name='Title for product', max_length=255)),
                ('product_description', models.CharField(help_text='product desc', default='Описание <product> из категории <category> от компании <company>', verbose_name='Description for product', max_length=255)),
                ('product_keywords', models.CharField(help_text='product keywords', default='ключевые слова, <product>, <company>, <category>', verbose_name='Keywords for product', max_length=255)),
                ('category_title', models.CharField(help_text='category title', default='купить <category> в Киеве недорого - <company>', verbose_name='Title for category', max_length=255)),
                ('category_description', models.CharField(help_text='category desc', default='Описание категории <category> от компании <company>', verbose_name='Description for category', max_length=255)),
                ('category_keywords', models.CharField(help_text='category keywords', default='ключевые слова, <company>, <category>', verbose_name='Keywords for category', max_length=255)),
                ('static_page_title', models.CharField(help_text='static title', default='Страница <page_name> - <company>', verbose_name='Title for static page', max_length=255)),
                ('static_page_description', models.CharField(help_text='static', default='Описание страницы <page_name> от компании <company>', verbose_name='Description for static page', max_length=255)),
                ('static_page_keywords', models.CharField(help_text='static keys', default='ключевые слова, <company>, <page_name>', verbose_name='Keywords for static page', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.SlugField(max_length=255)),
                ('namespace', models.SlugField(default='common', max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.TextField(verbose_name='Comment', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='galleryimageposition',
            name='gallery',
            field=models.ForeignKey(to='website.Gallery', related_name='images'),
        ),
        migrations.AlterUniqueTogether(
            name='variable',
            unique_together=set([('namespace', 'name')]),
        ),
    ]
