# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('goods_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='deli_address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deli_name', models.CharField(max_length=50)),
                ('detail_address', models.TextField()),
                ('postcode', models.CharField(max_length=6)),
                ('phone_number', models.CharField(max_length=11)),
                ('user_id', models.ForeignKey(to='login.user_info')),
            ],
            options={
                'db_table': 'deli_address',
            },
        ),
        migrations.CreateModel(
            name='order_record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goods_count', models.IntegerField()),
                ('goods_id', models.ForeignKey(to='goods_info.goods_info')),
            ],
            options={
                'db_table': 'order_record',
            },
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_time', models.DateTimeField(auto_now=True)),
                ('is_pay', models.BooleanField()),
                ('total_price', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('deli_id', models.ForeignKey(to='person_info.deli_address')),
                ('user_id', models.ForeignKey(to='login.user_info')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='recent_views',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_time', models.DateTimeField(auto_now=True)),
                ('goods_id', models.ForeignKey(to='goods_info.goods_info')),
                ('user_id', models.ForeignKey(to='login.user_info')),
            ],
            options={
                'db_table': 'recent_views',
            },
        ),
        migrations.AddField(
            model_name='order_record',
            name='order_id',
            field=models.ForeignKey(to='person_info.orders'),
        ),
    ]
