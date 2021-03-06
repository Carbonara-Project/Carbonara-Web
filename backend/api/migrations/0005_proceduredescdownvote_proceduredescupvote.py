# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-04 11:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_auto_20180202_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcedureDescDownvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proc_desc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProcedureDesc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcedureDescUpvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proc_desc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProcedureDesc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
