# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gadgetfreak_web', '0008_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='img_thumb',
        ),
    ]