# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-20 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20180406_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(upload_to='profile_image'),
        ),
    ]
