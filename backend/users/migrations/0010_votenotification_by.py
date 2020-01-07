# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-06 19:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_votenotification_creation_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='votenotification',
            name='by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_by_user_set', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
