import urllib, csv

from experimentlist.models import Experiment
from datetime import datetime


file_name = "experi_list.csv"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/"
data_source_url = "http://10.1.8.120:8000/report/data_source/csv/?experiment="


def search_experiments(search_term):
    """Retrieves the experiment table from the genotype database.

    Creates a Experiment model from each row where the name field
    matches the given search term.
    Does not save the models as the models should always be retrieved
    from the genotype database, not the website DB. Instead returns a
    list of the models

    :param search_term String of name where the results must match
    :return List of models.Experiment with name that matches search term.
            None (instead of empty list) if no matching name field on
            experiment table
    """
    with urllib.request.urlopen(experi_table_url) as experi_csv:
    # with open(file_name) as experi_csv:
        results = _search_table(experi_csv, search_term)
    if len(results) == 0:
        return None
    else:
        return results


def _search_table(experi_file, search_term):
    reader = csv.DictReader(experi_file)
    results = []
    for row in reader:
        if row['name'] == search_term:
            results.append(_create_experiment(row))
    return results


def _create_experiment(row):
    # Creates and returns an experiment model from the values in the row
    name = row['name']
    who = row['pi']
    when = row['createddate']
    ds = _get_data_source(name)
    return Experiment(
        name=name, primary_investigator=who, date_created=when
    )


def _get_data_source(name):
    ds_url = data_source_url + name
    with urllib.request.urlopen(ds_url) as ds:
        # TODO: Do stuff. No idea what it looks like until server lets me in again
        print("shalalala")


def _format_time(date_string):
    split_at_colon = date_string.split(":")
    front_rebuild = ":".join(split_at_colon[:-1])
    formatable_time = ''.join([front_rebuild, split_at_colon[-1]])
    datetime_time = datetime.strptime(formatable_time, "%Y-%m-%d %X.%f%z")
    return datetime_time.strftime('%d.%m.%Y %H:%M')