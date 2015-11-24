import urllib, csv

from experimentlist.models import DataSource
from datetime import datetime

ds_file_name = "ds.csv"
data_source_url = "http://10.1.8.167:8000/report/data_source/csv/?name="


def get_data_source(name):
    name_filter = name.replace(" ", "+")
    search_table = data_source_url + name_filter
    urllib.request.urlretrieve(search_table, ds_file_name)
    ds_csv = open(ds_file_name, 'r')
    return _create_datasources(ds_csv, name)


def _create_datasources(ds_file, search_term):
    reader = csv.DictReader(ds_file)
    results = []
    for row in reader:
        """ for some reason, ds_file is the whole table when the
        search_term doesn't match anything, so have to preform a check if
        this is the case"""
        if search_term not in row['name']:
            return None
        results.append(_create_datasource(row))
    return results


def _create_datasource(row):
    supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
    return DataSource(
        name=row['name'], is_active=row['is_active'], source=row['source'],
        supplier=row['supplier'], supply_date=supplieddate,
    )