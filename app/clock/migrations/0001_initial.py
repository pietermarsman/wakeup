# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-08 15:40
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('downloader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('download',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='downloader.Download')),
            ],
        ),
    ]
