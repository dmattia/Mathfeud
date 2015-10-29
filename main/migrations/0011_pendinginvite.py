# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20151029_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=50)),
                ('activation_key', models.CharField(max_length=40)),
                ('group', models.ForeignKey(to='main.GroupProfile')),
            ],
        ),
    ]
