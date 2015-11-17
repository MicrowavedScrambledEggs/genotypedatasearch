from django.db import models


class Experiment(models.Model):
    """Model for Experiment list

    contains the Name, Who?, When? and data source
    """
    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Data Source'
    ]

    name = models.CharField(field_names[0], max_length=200)
    primary_investigator = models.CharField(field_names[1], max_length=200)  # Who
    date_created = models.DateTimeField(field_names[2])  # When
    data_source = models.CharField(field_names[3], max_length=200, default="DS")  # TODO: Decide how to display this

    def __str__(self):
        return self.name
