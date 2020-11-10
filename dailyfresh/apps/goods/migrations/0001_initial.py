# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2020-10-21 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='单品名称')),
                ('detail', models.CharField(max_length=256, verbose_name='单品描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='商品价格')),
                ('count', models.IntegerField(default=1, verbose_name='库存')),
                ('unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('status', models.SmallIntegerField(choices=[(1, '上线'), (2, '售罄'), (0, '下架')], default=1, verbose_name='商品状态')),
                ('sales', models.IntegerField(default=0, verbose_name='销售数量')),
            ],
            options={
                'verbose_name': '单品信息',
                'verbose_name_plural': '单品信息',
                'db_table': 'Goods_info',
            },
        ),
        migrations.CreateModel(
            name='GoodsSPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('detail', models.CharField(max_length=256, verbose_name='SPU商品描述')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'GoodsSPU_info',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='种类名称')),
            ],
            options={
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
                'db_table': 'GoodsType',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSPU', verbose_name='商品SPU'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='商品种类'),
        ),
    ]
