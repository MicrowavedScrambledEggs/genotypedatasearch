from django.db import models


class Experiment(models.Model):
    """Model for Experiment list

    contains the Name, Who?, When? and data source
    """
    name = models.CharField(max_length=200)
    primary_investigator = models.CharField(max_length=200) #Who
    date_created = models.DateTimeField() #When
    data_source = models.CharField(max_length=200, default="DS") #TODO: Decide how to display this

    def __str__(self):
        return self.name