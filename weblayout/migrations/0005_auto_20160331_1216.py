# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0004_auto_20160328_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalmenu',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='additionalmenuitemdata',
            name='item',
        ),
        migrations.RemoveField(
            model_name='additionalmenuitemdata',
            name='language',
        ),
        migrations.RemoveField(
            model_name='extramenu',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='extramenuitemdata',
            name='item',
        ),
        migrations.RemoveField(
            model_name='extramenuitemdata',
            name='language',
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='mainmenuitemdata',
            name='item',
        ),
        migrations.RemoveField(
            model_name='mainmenuitemdata',
            name='language',
        ),
        migrations.DeleteModel(
            name='AdditionalMenu',
        ),
        migrations.DeleteModel(
            name='AdditionalMenuItemData',
        ),
        migrations.DeleteModel(
            name='ExtraMenu',
        ),
        migrations.DeleteModel(
            name='ExtraMenuItemData',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.DeleteModel(
            name='MainMenu',
        ),
        migrations.DeleteModel(
            name='MainMenuItemData',
        ),
    ]
