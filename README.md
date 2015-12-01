# genotypedatasearch
Web app for searching experimental genotype data, for use by Plant and Food Reasearch

Built with Django 1.8
To run server, from project directory enter command:
$ manage.py runserver [ip address with port]

Allows for searching by experiment name, primary investigator and date created.
Displays table of matching results, with links in each row to the relavant datasource 
table and a download link for the data.

Genotype data is currently queried externally, and not stored in this app's server
