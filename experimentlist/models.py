from django.db import models


class Experiment(models.Model):
    """Model for Experiment list

    contains the Name, Who?, When? and data source
    """
    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Data Source',
        'Download Link',
    ]

    name = models.CharField(field_names[0], max_length=200)
    primary_investigator = models.CharField(field_names[1], max_length=200)  # Who
    date_created = models.DateTimeField(field_names[2])  # When
    data_source = models.CharField(field_names[3], max_length=200)
    download_link = models.CharField(field_names[4], max_length=200)

    def __str__(self):
        return self.name


class DataSource(models.Model):

    name = models.CharField(max_length=200)
    is_active = models.CharField(max_length=200) # BoolFeild too fiddly
    source = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    supply_date = models.DateField()