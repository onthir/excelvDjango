# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-27 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0004_reviewlist_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compareFile1', to='analyze.File')),
                ('file2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compareFile2', to='analyze.File')),
            ],
        ),
    ]
