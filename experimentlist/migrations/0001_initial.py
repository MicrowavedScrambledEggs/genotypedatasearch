# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('primary_investigator', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField()),
                ('data_source', models.CharField(default='DS', max_length=200)),
            ],
        ),
    ]
