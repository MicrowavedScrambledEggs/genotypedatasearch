# genotypedatasearch
Web app for searching experimental genotype data (currently at database hosted at http://10.1.8.167:8000/report/), for use by Plant and Food Reasearch

Built with Django 1.8

To run server, from project directory enter command:
```shell
$ manage.py runserver [ip address with port]
```

Allows for searching by experiment name, primary investigator and date created.
Displays table of matching results, with links in each row to the relavant datasource 
table and a download link for the data.

Genotype data is currently queried externally (from http://10.1.8.167:8000/report/experiment/csv/), and not stored in this app's server

Datasource table got from querying via url: "http://10.1.8.167:8000/report/data_source/csv/?experiment=" + experiment_name

Download links are to: "http://10.1.8.167:8000/report/genotype/csv/?experiment=" + experiment_name

(Test use csv files in test_resources instead of http://10.1.8.167:8000/report/)
