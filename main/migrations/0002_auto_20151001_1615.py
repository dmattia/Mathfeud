# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='video',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
