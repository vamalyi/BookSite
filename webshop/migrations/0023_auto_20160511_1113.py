# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 08:13
from __future__ import unicode_literals

import ckeditor.fields
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0022_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name'], 'verbose_name': 'Manufacturer', 'verbose_name_plural': 'Manufacturers'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='h1_generation_rule',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_description_generation_rule',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_generation_rule',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='description',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='h1',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='meta_canonical',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='meta_robots',
        ),
        migrations.RemoveField(
            model_name='prefilter',
            name='title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title for page'),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title for page'),
        ),
        migrations.AlterField(
            model_name='category',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='first_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='First text'),
        ),
        migrations.AlterField(
            model_name='category',
            name='h1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='H1'),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_canonical',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='second_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Second text'),
        ),
        migrations.AlterField(
            model_name='category',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weblayout.Template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.CharField(max_length=256, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name of currency'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='short_name',
            field=models.CharField(max_length=3, verbose_name='Short name of currency'),
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='code',
            field=models.CharField(max_length=256, null=True, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='from_mass',
            field=models.FloatField(blank=True, null=True, verbose_name='From mass'),
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='deliveryrule',
            name='to_mass',
            field=models.FloatField(blank=True, null=True, verbose_name='To mass'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='margin',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='margin',
            name='percent',
            field=models.FloatField(verbose_name='Percent'),
        ),
        migrations.AlterField(
            model_name='parameterrange',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight of parameter range'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='first_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='First text'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name of prefilter'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='original_url',
            field=models.CharField(max_length=1024, verbose_name='Original URL'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='second_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Secord text'),
        ),
        migrations.AlterField(
            model_name='prefilter',
            name='url',
            field=models.CharField(max_length=256, unique=True, verbose_name='URL of prefilter'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Status product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=256, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_on_add',
            field=models.DateTimeField(auto_now=True, verbose_name='Last updated date and time'),
        ),
        migrations.AlterField(
            model_name='product',
            name='default_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Default price of product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='first_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='First text'),
        ),
        migrations.AlterField(
            model_name='product',
            name='h1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='H1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Is new product?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_top',
            field=models.BooleanField(default=False, verbose_name='Is top product?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='margin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.Margin', verbose_name='Margin'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mass',
            field=models.FloatField(default=0, verbose_name='Mass of product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_canonical',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Provider', verbose_name='Provider'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.Sale', verbose_name='Sale'),
        ),
        migrations.AlterField(
            model_name='product',
            name='second_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Second text'),
        ),
        migrations.AlterField(
            model_name='product',
            name='special_proposition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.SpecialProposition', verbose_name='Special proposition'),
        ),
        migrations.AlterField(
            model_name='product',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weblayout.Template', verbose_name='Alternative template'),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.CharField(max_length=256, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight of product'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_large',
            field=image_cropping.fields.ImageRatioField('image_original', '0x0', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Large image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_medium',
            field=image_cropping.fields.ImageRatioField('image_original', '0x0', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Medium image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='cropping_small',
            field=image_cropping.fields.ImageRatioField('image_original', '0x0', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Small image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='image_large',
            field=models.CharField(blank=True, editable=False, max_length=256, null=True, verbose_name='Large image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='image_medium',
            field=models.CharField(blank=True, editable=False, max_length=256, null=True, verbose_name='Medium image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='image_original',
            field=models.ImageField(upload_to='image_positions/products/', verbose_name='Original image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='image_small',
            field=models.CharField(blank=True, editable=False, max_length=256, null=True, verbose_name='Small image'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='last_edit_date',
            field=models.DateField(auto_now=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='webshop.Product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='productimageposition',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_parameter/', verbose_name='First image of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Product parameter name'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='prefix',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_parameter/', verbose_name='Second image of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='suffix',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Suffix'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='first_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_parameter_value/', verbose_name='First image'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='product_parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='webshop.ProductParameter', verbose_name='Product parameter'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='second_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_parameter_value/', verbose_name='Second image'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='value',
            field=models.CharField(max_length=256, verbose_name='Value of parameter'),
        ),
        migrations.AlterField(
            model_name='productparameteravailablevalue',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight of parameter value'),
        ),
        migrations.AlterField(
            model_name='productparametervalue',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='productparametervalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_values', to='webshop.Product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productpricecorrector',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Name of product price corrector'),
        ),
        migrations.AlterField(
            model_name='productpricecorrector',
            name='new_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price of corrector'),
        ),
        migrations.AlterField(
            model_name='productpricecorrector',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_correctors', to='webshop.Product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='body',
            field=models.TextField(verbose_name='Review'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='date_created',
            field=models.DateField(auto_now=True, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='email',
            field=models.CharField(blank=True, max_length=256, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='name',
            field=models.CharField(blank=True, max_length=256, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='webshop.Product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='coefficient',
            field=models.FloatField(verbose_name='Coefficient to main currency'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Currency', verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name of provider'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sales/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='percent',
            field=models.FloatField(verbose_name='Percent'),
        ),
        migrations.AlterField(
            model_name='specialproposition',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='special_propositions/', verbose_name='Image of special proposition'),
        ),
        migrations.AlterField(
            model_name='specialproposition',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Special proposition name'),
        ),
    ]