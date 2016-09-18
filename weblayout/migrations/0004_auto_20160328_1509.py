# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblayout', '0003_auto_20160328_1235'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='additionalmenu',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='extramenu',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='mainmenu',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='menuitem',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(to='weblayout.Menu', related_name='items'),
        ),
    ]
