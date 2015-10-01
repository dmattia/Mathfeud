# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='grade',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
    ]
