import urllib, csv

from experimentlist.models import Experiment
from datetime import datetime


file_name = "experi_list.csv"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/?name="
data_source_url = "data_source/?name="
download_url = "http://10.1.8.167:8000/report/genotype/csv/?experiment="


def query_experiments(search_term):
    """
    Queries the experiment table in the genotype database with search_term
    as a contains filter for the name field.
    Creates a Experiment model from each row returned.

    Does not save the models as the models should always be retrieved
    from the genotype database, not the website DB. Instead returns a
    list of the models

    :param search_term String of name where the results must match
    :return List of models.Experiment with name that matches search term.
            None (instead of empty list) if no matching name field on
            experiment table
    """
    # Build url for query
    name_filter = search_term.replace(" ", "+")
    search_table = experi_table_url + name_filter
    # Make query
    urllib.request.urlretrieve(search_table, file_name)
    experi_csv = open(file_name, 'r')
    # Check if query returned anything
    if "No Data" in experi_csv.readline():
        return None

    experi_csv = open(file_name, 'r')
    return _create_experiments(experi_csv, search_term)


def _create_experiments(experi_file):
    # Creates and returns a list of models.Experiment from the given csv file
    reader = csv.DictReader(experi_file)
    results = []
    for row in reader:
        results.append(_create_experiment(row))
    return results


def _create_experiment(row):
    # Creates and returns an experiment model from the values in the row
    name = row['name']
    who = row['pi']
    when = _string_to_datetime(row['createddate'])
    ds = data_source_url + name.replace(" ", "+")
    dl = download_url + name.replace(" ", "+")
    return Experiment(
        name=name, primary_investigator=who, date_created=when,
        download_link=dl, data_source=ds,
    )


def _string_to_datetime(date_string):
    """
    createddate field values in the database have a colon in the UTC info,
    preventing a simple call of just strptime(). Removes colon in UTC info
    so can create a datetime from strptime
    :param date_string: Date string from createddate field
    :return: datetime from processed date string
    """
    # removing the colon from the UTC info (the last colon)
    split_at_colon = date_string.split(":")
    front_rebuild = ":".join(split_at_colon[:-1])
    formatable_time = ''.join([front_rebuild, split_at_colon[-1]])

    return datetime.strptime(formatable_time, "%Y-%m-%d %X.%f%z")