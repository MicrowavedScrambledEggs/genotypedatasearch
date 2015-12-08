import uuid
from django.db import models
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class Experiment(Model):
    """Model for Experiment list

    contains the Name, Who?, When? and data source
    """

    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Data Source',
        'Download Link',
    ]

    name = columns.Text(index=True,  max_length=200)
    primary_investigator = columns.Text(index=True)  # Who
    date_created = columns.TimeUUID(primary_key=True)  # When
    data_source = columns.Text(max_length=200)
    download_link = columns.Text(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'experimentsearch'


class ExperimentForTable(models.Model):

    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Data Source',
        'Download Link',
    ]

    name = models.CharField(field_names[0], max_length=200)
    primary_investigator = models.CharField(field_names[1], max_length=200)  # Who
    date_created = models.DateTimeField(field_names[2])  # When
    data_source = models.CharField(field_names[3], max_length=200)
    download_link = models.CharField(field_names[4], max_length=200)

    class Meta:
        app_label = 'experimentsearch'


def make_table_experiment(experiment):
    return ExperimentForTable(
        name=experiment.name, primary_investigator=experiment.primary_investigator,
        date_created=experiment.date_created, data_source=experiment.data_source,
        download_link=experiment.download_link,
    )


class DataSource(Model):

    field_names = [
        'name', 'is_active', 'source', 'supplier', 'supply_date'
    ]

    name = columns.Text(primary_key=True, max_length=200)
    is_active = columns.Text(max_length=200) # BoolFeild too fiddly
    source = columns.Text(primary_key=True, max_length=200)
    supplier = columns.Text(max_length=200)
    supply_date = columns.Date()

    def __str__(self):
        return self.source

    class Meta:
        app_label = 'experimentsearch'


class DataSourceForTable(models.Model):

    field_names = [
        'name', 'is_active', 'source', 'supplier', 'supply_date'
    ]

    name = models.CharField(max_length=200)
    is_active = models.CharField(max_length=200) # BoolFeild too fiddly
    source = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    supply_date = models.DateField()

    class Meta:
        app_label = 'experimentsearch'