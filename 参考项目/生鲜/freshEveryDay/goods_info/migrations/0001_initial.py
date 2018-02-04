# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='goods_cate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('img_url', models.ImageField(upload_to=b'upload/')),
            ],
            options={
                'db_table': 'goods_cate',
            },
        ),
        migrations.CreateModel(
            name='goods_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.IntegerField()),
                ('img_url', models.ImageField(upload_to=b'upload/')),
                ('intro', models.TextField()),
                ('desc', tinymce.models.HTMLField()),
                ('unit', models.CharField(max_length=20)),
                ('sales_num', models.IntegerField(default=0)),
                ('putaway_date', models.DateTimeField(auto_now=True)),
                ('cate_id', models.ForeignKey(to='goods_info.goods_cate')),
            ],
            options={
                'db_table': 'goods_info',
            },
        ),
    ]
