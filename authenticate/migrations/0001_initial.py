# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 14:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'', verbose_name='\u041f\u0440\u043e\u0444\u0430\u0439\u043b \u0437\u0443\u0440\u0430\u0433')),
                ('cover_picture', models.ImageField(null=True, upload_to=b'', verbose_name='\u041a\u043e\u0432\u0435\u0440 \u0437\u0443\u0440\u0430\u0433')),
                ('career', models.CharField(max_length=50, null=True, verbose_name='\u041c\u044d\u0440\u0433\u044d\u0436\u0438\u043b')),
                ('about_me', models.TextField(null=True, verbose_name='\u041c\u0438\u043d\u0438\u0439 \u0442\u0443\u0445\u0430\u0439')),
                ('phone', models.IntegerField(null=True, verbose_name='Phone')),
                ('facebook', models.CharField(max_length=50, null=True, verbose_name='Facebook')),
                ('twitter', models.CharField(max_length=50, null=True, verbose_name='Twitter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
