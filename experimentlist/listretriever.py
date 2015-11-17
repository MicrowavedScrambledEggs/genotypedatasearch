import urllib, io, csv

from experimentlist.models import Experiment

"""Retrieves the experiment table from the database.

Creates a Experiment model from each row
"""

file_name = "experi_list.csv"


def retrieve_list(experi_table_url):
    # Type checking
    if not isinstance(experi_table_url, str):
        raise TypeError("str of url required: " + experi_table_url.str()
                        + "is of type " + experi_table_url.type())

    # Clear all the previous Experiment models
    """ TODO: Can imagine with a big list of experiments it would be more
      efficient to only update changed rows and add new rows, instead of
       deleting and refetching"""
    Experiment.objects.all().delete()

    # get the table and save to a file
    urllib.request.urlretrieve(experi_table_url, file_name)
    experi_file = open(file_name)
    _create_experiment_models(experi_file)


def _create_experiment_models(experi_file):
    reader = csv.DictReader(experi_file)
    for row in reader:
        _create_experiment_model(row)


def _create_experiment_model(row):
    # Creates and saves an experiment model from the values in the row
    name = row['name']
    who = row['pi']
    when = row['createddate']
    experi = Experiment(name=name, primary_investigator=who,
                        date_created=when)
    experi.save()
