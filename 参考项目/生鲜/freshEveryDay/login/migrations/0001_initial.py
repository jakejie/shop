# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('passwd', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=11, null=True, blank=True)),
                ('registe_date', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]
