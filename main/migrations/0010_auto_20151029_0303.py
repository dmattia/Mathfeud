# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_pendinginvite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendinginvite',
            name='group',
        ),
        migrations.DeleteModel(
            name='PendingInvite',
        ),
    ]
