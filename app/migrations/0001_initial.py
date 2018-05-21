# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('file_type', models.CharField(max_length=10)),
                ('file_content', models.FileField(upload_to=b'files/')),
            ],
        ),
        migrations.CreateModel(
            name='Sentiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=200)),
                ('created_at', models.CharField(max_length=30, null=True)),
                ('collected_at', models.DateField()),
                ('sent_accuracy', models.FloatField(null=True)),
                ('sentiment', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='app.Sentiment', null=True)),
            ],
        ),
    ]
