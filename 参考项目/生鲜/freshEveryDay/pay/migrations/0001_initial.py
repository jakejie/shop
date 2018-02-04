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
            name='cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy_count', models.IntegerField()),
                ('goods_id', models.ForeignKey(to='goods_info.goods_info')),
                ('user_id', models.ForeignKey(to='login.user_info')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
