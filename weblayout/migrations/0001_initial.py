# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url_type', models.CharField(max_length=256, choices=[('splitter', 'None'), ('static_page', 'Static Page'), ('category', 'Category'), ('product', 'Product'), ('pre_filter', 'PreFilter'), ('custom', 'External Link')])),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='additional_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='additional_menu/')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='weblayout.AdditionalMenu', blank=True, related_name='children', null=True)),
            ],
            options={
                'verbose_name_plural': 'Additional Menu',
                'db_table': 'additional_menu',
                'verbose_name': 'Additional Menu Element',
            },
        ),
        migrations.CreateModel(
            name='AdditionalMenuItemData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('item', models.ForeignKey(to='weblayout.AdditionalMenu')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url_type', models.CharField(max_length=256, choices=[('splitter', 'None'), ('static_page', 'Static Page'), ('category', 'Category'), ('product', 'Product'), ('pre_filter', 'PreFilter'), ('custom', 'External Link')])),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='extra_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='extra_menu/')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='weblayout.ExtraMenu', blank=True, related_name='children', null=True)),
            ],
            options={
                'verbose_name_plural': 'Extra Menu',
                'db_table': 'extra_menu',
                'verbose_name': 'Extra Menu Element',
            },
        ),
        migrations.CreateModel(
            name='ExtraMenuItemData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('item', models.ForeignKey(to='weblayout.ExtraMenu')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('short_name', models.CharField(max_length=2)),
                ('default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url_type', models.CharField(max_length=256, choices=[('splitter', 'None'), ('static_page', 'Static Page'), ('category', 'Category'), ('product', 'Product'), ('pre_filter', 'PreFilter'), ('custom', 'External Link')])),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='main_menu/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='main_menu/')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='weblayout.MainMenu', blank=True, related_name='children', null=True)),
            ],
            options={
                'verbose_name_plural': 'Main Menu',
                'db_table': 'main_menu',
                'verbose_name': 'Main Menu Element',
            },
        ),
        migrations.CreateModel(
            name='MainMenuItemData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, null=True, default=None, max_length=256)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('item', models.ForeignKey(to='weblayout.MainMenu')),
                ('language', models.ForeignKey(to='weblayout.Language')),
            ],
        ),
        migrations.CreateModel(
            name='SystemElement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, unique=True, choices=[('Header', 'Header'), ('Footer', 'Footer'), ('Script', 'Script')])),
                ('body', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'System Elements',
                'db_table': 'system_elements',
                'verbose_name': 'System Element',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('path', models.CharField(unique=True, max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Templates',
                'db_table': 'templates',
                'verbose_name': 'Template',
            },
        ),
        migrations.AddField(
            model_name='extramenuitemdata',
            name='language',
            field=models.ForeignKey(to='weblayout.Language'),
        ),
        migrations.AddField(
            model_name='additionalmenuitemdata',
            name='language',
            field=models.ForeignKey(to='weblayout.Language'),
        ),
    ]
