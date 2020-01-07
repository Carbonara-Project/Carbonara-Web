# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-15 19:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180313_0148'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programcomment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='programcomment',
            name='program',
        ),
        migrations.RemoveField(
            model_name='programcomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='ProgramComment',
        ),
    ]
