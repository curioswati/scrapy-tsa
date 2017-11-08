# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='twitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('last_hq', models.FloatField()),
                ('last_tweet_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Usermodel',
            fields=[
                ('username', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('userpic', models.URLField(max_length=80)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='twitter',
            name='username',
            field=models.ForeignKey(to='app.Usermodel'),
        ),
    ]
