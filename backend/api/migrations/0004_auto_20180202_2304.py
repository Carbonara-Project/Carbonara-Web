# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-02 23:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_proceduredesccomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcedureDescCommentDownvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcedureDescCommentUpvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='proceduredesccomment',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='proceduredesccomment',
            name='upvotes',
        ),
        migrations.AddField(
            model_name='proceduredesccommentupvote',
            name='proc_desc_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProcedureDescComment'),
        ),
        migrations.AddField(
            model_name='proceduredesccommentupvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proceduredesccommentdownvote',
            name='proc_desc_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProcedureDescComment'),
        ),
        migrations.AddField(
            model_name='proceduredesccommentdownvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
