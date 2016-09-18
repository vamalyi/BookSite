# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields
import ckeditor.fields
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('url', models.CharField(unique=True, max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('first_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('second_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('title_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_description_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('h1_generation_rule', models.CharField(blank=True, null=True, max_length=256)),
                ('template', models.ForeignKey(to='weblayout.Template')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('short_name', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'db_table': 'currencies',
                'verbose_name': 'Currency',
            },
        ),
        migrations.CreateModel(
            name='DeliveryRule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('from_mass', models.FloatField(blank=True, null=True)),
                ('to_mass', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Delivery Rules',
                'db_table': 'delivery_rules',
                'verbose_name': 'Delivery Rule',
            },
        ),
        migrations.CreateModel(
            name='Margin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('percent', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Margins',
                'db_table': 'margins',
                'verbose_name': 'Margin',
            },
        ),
        migrations.CreateModel(
            name='PreFilter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('url', models.CharField(unique=True, max_length=256)),
                ('title', models.CharField(blank=True, null=True, max_length=256)),
                ('first_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('second_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('original_url', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name_plural': 'PreFilters',
                'db_table': 'pre_filters',
                'verbose_name': 'PreFilter',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(unique=True, max_length=256)),
                ('url', models.CharField(unique=True, max_length=256)),
                ('title', models.CharField(blank=True, null=True, max_length=256)),
                ('default_price', models.FloatField()),
                ('active', models.BooleanField(default=True)),
                ('first_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('is_top', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=False)),
                ('second_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('meta_description', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_canonical', models.CharField(blank=True, null=True, max_length=256)),
                ('meta_robots', models.CharField(blank=True, null=True, max_length=256)),
                ('h1', models.CharField(blank=True, null=True, max_length=256)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('date_on_add', models.DateTimeField(auto_now=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField(default=0)),
                ('mass', models.FloatField(default=0)),
                ('category', models.ForeignKey(to='webshop.Category')),
                ('margin', models.ForeignKey(to='webshop.Margin', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'products',
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductImagePosition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_original', models.ImageField(upload_to='image_positions/products/')),
                ('cropping_large', image_cropping.fields.ImageRatioField('image_original', '960x680', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping large', hide_image_field=False, adapt_rotation=False)),
                ('cropping_medium', image_cropping.fields.ImageRatioField('image_original', '162x122', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping medium', hide_image_field=False, adapt_rotation=False)),
                ('cropping_small', image_cropping.fields.ImageRatioField('image_original', '62x44', free_crop=False, allow_fullsize=False, help_text=None, size_warning=False, verbose_name='cropping small', hide_image_field=False, adapt_rotation=False)),
                ('image_large', models.CharField(blank=True, max_length=256, null=True, editable=False)),
                ('image_medium', models.CharField(blank=True, max_length=256, null=True, editable=False)),
                ('image_small', models.CharField(blank=True, max_length=256, null=True, editable=False)),
                ('name', models.CharField(max_length=256)),
                ('title', models.CharField(blank=True, null=True, max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('weight', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, null=True, max_length=256)),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Image Positions',
                'db_table': 'product_image_positions',
                'verbose_name': 'Product Image Position',
            },
        ),
        migrations.CreateModel(
            name='ProductParameter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='product_parameter/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='product_parameter/')),
                ('prefix', models.CharField(blank=True, null=True, max_length=8)),
                ('suffix', models.CharField(blank=True, null=True, max_length=8)),
                ('weight', models.IntegerField()),
                ('category', models.ForeignKey(to='webshop.Category')),
            ],
            options={
                'verbose_name_plural': 'Product Parameters',
                'db_table': 'product_parameters',
                'verbose_name': 'Product Parameter',
            },
        ),
        migrations.CreateModel(
            name='ProductParameterAvailableValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=256)),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='product_parameter_value/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='product_parameter_value/')),
                ('weight', models.IntegerField()),
                ('product_parameter', models.ForeignKey(to='webshop.ProductParameter')),
            ],
            options={
                'verbose_name_plural': 'Product Parameter Available Values',
                'db_table': 'product_parameters_available_value',
                'verbose_name': 'Product Parameter Available Value',
            },
        ),
        migrations.CreateModel(
            name='ProductParameterValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('category', models.ForeignKey(to='webshop.Category')),
                ('product', models.ForeignKey(to='webshop.Product')),
                ('product_parameter', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', to='webshop.ProductParameter')),
                ('value', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='product_parameter', chained_model_field='product_parameter', to='webshop.ProductParameterAvailableValue', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Product Parameter Values',
                'db_table': 'product_parameters_values',
                'verbose_name': 'Product Parameter Value',
            },
        ),
        migrations.CreateModel(
            name='ProductPriceCorrector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('new_price', models.FloatField()),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Price Corrections',
                'db_table': 'product_price_correctors',
                'verbose_name': 'Product Price Correction',
            },
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('comment', ckeditor.fields.RichTextField()),
                ('rating', models.FloatField()),
                ('state', models.BooleanField(default=False)),
                ('date_on_add', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
            options={
                'verbose_name_plural': 'Rating and comment for product',
                'db_table': 'product_ratings',
                'verbose_name': 'Ratings and comments for product',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('coefficient', models.FloatField()),
                ('currency', models.ForeignKey(to='webshop.Currency')),
            ],
            options={
                'verbose_name_plural': 'Providers',
                'db_table': 'providers',
                'verbose_name': 'Provider',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('percent', models.FloatField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='sales/')),
            ],
            options={
                'verbose_name_plural': 'Sales',
                'db_table': 'sales',
                'verbose_name': 'Sale',
            },
        ),
        migrations.CreateModel(
            name='SpecialProposition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('image', models.ImageField(blank=True, verbose_name='special_propositions/', null=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Special Propositions',
                'db_table': 'special_propositions',
                'verbose_name': 'Special Proposition',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='webshop.Provider'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.ForeignKey(to='webshop.Sale', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='special_proposition',
            field=models.ForeignKey(to='webshop.SpecialProposition', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='template',
            field=models.ForeignKey(to='weblayout.Template'),
        ),
        migrations.AlterUniqueTogether(
            name='productpricecorrector',
            unique_together=set([('product', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparametervalue',
            unique_together=set([('product', 'category', 'product_parameter', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparameteravailablevalue',
            unique_together=set([('product_parameter', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='productparameter',
            unique_together=set([('name', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='productimageposition',
            unique_together=set([('product', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'category')]),
        ),
    ]
