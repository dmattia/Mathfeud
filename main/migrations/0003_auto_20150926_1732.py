# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150922_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.ForeignKey(to='main.GroupProfile'),
        ),
    ]
