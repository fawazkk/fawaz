# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-30 14:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_conclusion'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['timestamp', '-updated']},
        ),
    ]
