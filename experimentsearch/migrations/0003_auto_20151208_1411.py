# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentsearch', '0002_auto_20151126_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSourceForTable',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentForTable',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DataSource',
        ),
        migrations.DeleteModel(
            name='Experiment',
        ),
    ]
