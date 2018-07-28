# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-27 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0005_compare'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compare',
            name='file1',
        ),
        migrations.RemoveField(
            model_name='compare',
            name='file2',
        ),
        migrations.AddField(
            model_name='compare',
            name='files',
            field=models.ManyToManyField(related_name='compareFile1', to='analyze.File'),
        ),
        migrations.AddField(
            model_name='compare',
            name='title',
            field=models.CharField(default=None, max_length=500),
            preserve_default=False,
        ),
    ]