# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-10-21 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20201021_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodssku',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '下架'), (1, '上线'), (2, '售罄')], default=1, verbose_name='商品状态'),
        ),
    ]
