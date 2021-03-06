# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-07 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='Top40Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('artist', models.CharField(max_length=512)),
                ('first_appeared', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeClip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='downloader.Top40Song')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='top40song',
            unique_together=set([('title', 'artist')]),
        ),
        migrations.AddField(
            model_name='download',
            name='clip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='downloader.YoutubeClip'),
        ),
    ]
