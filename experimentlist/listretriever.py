import urllib, csv

from experimentlist.models import Experiment
from datetime import datetime


file_name = "experi_list.csv"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/?name="
data_source_url = "http://10.1.8.120:8000/report/data_source/csv/?experiment="


def search_experiments(search_term):
    """Retrieves the rows in the experiment table from the genotype
    database using the search_term as a contains filter for the name
    field. Creates a Experiment model from each row.

    Does not save the models as the models should always be retrieved
    from the genotype database, not the website DB. Instead returns a
    list of the models

    :param search_term String of name where the results must match
    :return List of models.Experiment with name that matches search term.
            None (instead of empty list) if no matching name field on
            experiment table
    """
    name_filter = _process_search_term(search_term)
    search_table = experi_table_url + name_filter
    urllib.request.urlretrieve(search_table, file_name)
    experi_csv = open(file_name, 'r')
    return _create_experiments(experi_csv, search_term)


def _process_search_term(search_term):
    terms = search_term.split(" ")
    return "+".join(terms)


def _create_experiments(experi_file, search_term):
    reader = csv.DictReader(experi_file)
    results = []
    for row in reader:
        """ for some reason, experi_file is the whole table when the
        search_term doesn't match anything, so have to preform a check if
        this is the case"""
        if search_term not in row['name']:
            return None
        results.append(_create_experiment(row))
    return results


def _create_experiment(row):
    # Creates and returns an experiment model from the values in the row
    name = row['name']
    who = row['pi']
    when = row['createddate']
    # ds = _get_data_source(name)
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