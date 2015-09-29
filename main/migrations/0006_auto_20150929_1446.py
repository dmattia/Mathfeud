# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_video_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='main.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='likes',
        ),
        migrations.AddField(
            model_name='like',
            name='video',
            field=models.ForeignKey(to='main.Video'),
        ),
    ]
