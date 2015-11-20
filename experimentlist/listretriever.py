import urllib, csv

from experimentlist.models import Experiment
from datetime import datetime

"""Retrieves the experiment table from the database.

Creates a Experiment model from each row
"""

file_name = "experi_list.csv"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/"


def search_experiments(search_term):
    # with urllib.request.urlopen(experi_table_url) as experi_csv:
    with open(file_name) as experi_csv:
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
    return Experiment(
        name=name, primary_investigator=who, date_created=when
    )


def _format_time(date_string):
    split_at_colon = date_string.split(":")
    front_rebuild = ":".join(split_at_colon[:-1])
    formatable_time = ''.join([front_rebuild, split_at_colon[-1]])
    datetime_time = datetime.strptime(formatable_time, "%Y-%m-%d %X.%f%z")
    return datetime_time.strftime('%d.%m.%Y %H:%M')