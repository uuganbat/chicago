# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='view',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]