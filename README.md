# genotypedatasearch
Web app for searching experimental genotype data (currently at database hosted at http://10.1.8.167:8000/report/), for use by Plant and Food Reasearch

Built with Django 1.8

Requires libraries:
- pymongo 2.8
- mongoengine 0.9

These out-of-date versions are required as the Django extension was removed from mongoengine 1.x (as of writing there was no stable replacement), and pymongo 3.x is only apparently compatible with mongoengine 1.x

To run server, from project directory enter command:
```shell
$ manage.py runserver [ip address with port]
```

Allows for searching by experiment name, primary investigator and date created.
Displays table of matching results, with links in each row to the relevant datasource
table and a download link for the data.

On start up, syncs local db with http://10.1.8.167:8000/report/experiment/csv/

Datasource table got from querying via url: "http://10.1.8.167:8000/report/data_source/csv/?experiment=" + experiment_name

Download links are to: "http://10.1.8.167:8000/report/genotype/csv/?experiment=" + experiment_name

(Test use csv files in test_resources instead of http://10.1.8.167:8000/report/)
