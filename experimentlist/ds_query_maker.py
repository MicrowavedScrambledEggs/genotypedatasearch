import urllib, csv

from experimentlist.models import DataSource
from datetime import datetime

# TODO: Very similar to experiment_query_maker.py so should strategy pattern this
# if have to make another something_query_maker
ds_file_name = "ds.csv"
data_source_url = "http://10.1.8.167:8000/report/data_source/csv/?experiment="


def query_data_source(name):
    """
    Queries the data_source table in the genotype database for rows associated
    with an experiment that matches the given name. Creates and returns a list
    of models.DataSource from the rows returned by the query.

    Does NOT .save() the models

    :param name: Name of experiment to query for associations
    :return: List of models.DataSource built from query results. None (instead
             of empty list) if query does not return anything
    """
    # Build Query url
    name_filter = name.replace(" ", "+")
    search_table = data_source_url + name_filter
    # Make query
    urllib.request.urlretrieve(search_table, ds_file_name)
    # Check if query returned anything
    ds_csv = open(ds_file_name, 'r')
    if 'No Data' in ds_csv.readline():
        return None

    ds_csv = open(ds_file_name, 'r')
    return _create_datasources(ds_csv)


def _create_datasources(ds_file):
    # Create list of models.DataSource from the given file
    reader = csv.DictReader(ds_file)
    results = []
    for row in reader:
        results.append(_create_datasource(row))
    return results


def _create_datasource(row):
    # Creates a models.DataSource from the values in the given row
    # TODO: Put this method in the strategy if I make one
    supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
    return DataSource(
        name=row['name'], is_active=row['is_active'], source=row['source'],
        supplier=row['supplier'], supply_date=supplieddate,
    )
