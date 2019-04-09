# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 07:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='\u0410\u043d\u0433\u0438\u043b\u0430\u043b')),
                ('slug', models.CharField(max_length=50, verbose_name='Slug')),
                ('icon', models.CharField(max_length=50, verbose_name='Icon')),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='\u0413\u0430\u0440\u0447\u0438\u0433')),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u0417\u0443\u0440\u0430\u0433')),
                ('audio', models.FileField(upload_to=b'', verbose_name='Audio')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.Category', verbose_name='\u0410\u043d\u0433\u0438\u043b\u0430\u043b')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created_by')),
            ],
        ),
    ]
