# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentsearch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('supplier', models.CharField(max_length=200)),
                ('supply_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='download_link',
            field=models.CharField(verbose_name='Download Link', default='download/', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experiment',
            name='data_source',
            field=models.CharField(verbose_name='Data Source', max_length=200),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=200),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='primary_investigator',
            field=models.CharField(verbose_name='Primary Investigator', max_length=200),
        ),
    ]
