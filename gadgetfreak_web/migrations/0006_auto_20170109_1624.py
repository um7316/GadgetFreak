# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gadgetfreak_web', '0005_forumtopic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumtopic',
            name='topic_type',
            field=models.CharField(choices=[('R', 'Review'), ('C', 'Comment')], default='C', max_length=1),
        ),
    ]
