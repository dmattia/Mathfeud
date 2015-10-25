# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151001_2015'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Video',
        ),
    ]
