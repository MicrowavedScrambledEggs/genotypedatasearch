import csv, urllib

from django.shortcuts import render
from django.http import StreamingHttpResponse
from django_tables2 import RequestConfig

from .query_maker import QueryMaker
from .query_strategy import ExperimentQueryStrategy, DataSourceQueryStrategy
from .tables import ExperimentTable, DataSourceTable
from . import forms as my_forms
from .models import Experiment

genotype_url = "http://10.1.8.167:8000/report/genotype/csv/"
data_source_url = "http://10.1.8.167:8000/report/data_source/csv/"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/"
genotype_file_name = 'experiment.csv'
experi_query_prefix = "?experiment="
name_query_prefix = "?name="
pi_query_prefix = "?pi="
date_query_prefix = "?date="

def index(request):
    """
    Renders the search page according to the index.html template, with a
    form.SearchForm as the search form.

    If the search form has any GET data, retrieves models.Experiment that
    match the GET data to populate a table

    :param request:
    :return:
    """
    if request.method == 'GET':
        form = my_forms.NameSearchForm()
        type_select = my_forms.SearchTypeSelect()
        search_list = None
        search_term = None
        if 'search_by' in request.GET:
            type_select = my_forms.SearchTypeSelect(request.GET)
            form = choose_form(request.GET['search_by'])
        if 'search_name' in request.GET:
            form = my_forms.NameSearchForm(request.GET)
            search_term = request.GET['search_name'].strip()
            search_list = Experiment.objects.filter(name__contains=search_term)
        elif 'search_pi' in request.GET:
            form = my_forms.PISearchForm(request.GET)
            search_term = request.GET['search_pi'].strip()
            search_list = Experiment.objects.filter(primary_investigator__contains=search_term)
            type_select = my_forms.SearchTypeSelect(
                initial={'search_by': Experiment.field_names[1]}
            )
        elif 'from_date_month' in request.GET:
            # TODO: Need to check with Helge how he'll do date querires
            form = my_forms.DateSearchForm(request.GET)
            if form.is_valid():
                search_term = request.GET['from_date_month']
                search_list = make_experiment_query(search_term, date_query_prefix)
                type_select = my_forms.SearchTypeSelect(
                    initial={'search_by': Experiment.field_names[2]}
                )
        if search_list is None:
            table = None
        else:
            table = ExperimentTable(search_list)
            RequestConfig(request, paginate={"per_page": 25}).configure(table)
        context = {
            'search_form': form, 'search_term': search_term,
            'table': table, 'search_select': type_select
        }
        return render(
            request, 'experimentsearch/index.html', context
        )
    else:
        return render(
            request, 'experimentsearch/index.html',
            {'search_form': my_forms.NameSearchForm(),
             'search_select': my_forms.SearchTypeSelect()}
        )


def choose_form(search_by):
    if search_by == Experiment.field_names[2]:
        return my_forms.DateSearchForm()
    elif search_by == Experiment.field_names[1]:
        return my_forms.PISearchForm()
    else:
        return my_forms.NameSearchForm()


def make_experiment_query(search_term, prefix):
    query_maker = QueryMaker(ExperimentQueryStrategy)
    query_url = experi_table_url + prefix
    return query_maker.make_query(search_term, query_url)


def datasource(request):
    """
    Renders a data source table page according to the datasource.html template

    Populates a table with models.DataSource from a data_source table query
    using the name field in the GET data.

    Provides a link for the 'back to search' buttons from the from field in the
    GET data if there is one
    :param request:
    :return:
    """
    if request.method == 'GET':
        if 'from' in request.GET:
            from_page = request.GET['from']
        else:
            from_page = None
        if 'name' in request.GET:
            ds_name = request.GET['name']
            query_maker = QueryMaker(DataSourceQueryStrategy())
            ds_list = query_maker.make_query(ds_name, data_source_url)
            if ds_list is None:
                table = None
            else:
                table = DataSourceTable(ds_list)
                RequestConfig(request, paginate={"per_page": 25}).configure(table)
            return render(
                request, 'experimentsearch/datasource.html',
                {'table': table, 'ds_name': ds_name, 'from': from_page}
            )
    return render(request, 'experimentsearch/datasource.html', {})


class Echo(object):
    """Copied from docs.djangoproject.com/en/1.8/howto/outputting-csv/

    An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def stream_experiment_csv(request, experi_name):
    """
    Queries the genotype table with the experi_name as an experiment filter
    Saves the result to a csv file. Uses that file to write a http response
    which downloads the csv file for the client
    :param request:
    :param experi_name: name of experiment to query for associations
    :return: httpresponse that downloads results of query as csv
    """
    # Make query
    urllib.request.urlretrieve(genotype_url + experi_name, genotype_file_name)

    experiment_csv = open(genotype_file_name, 'r')
    reader = csv.reader(experiment_csv)
    writer = csv.writer(Echo())
    # Write query results to csv response
    response = StreamingHttpResponse((writer.writerow(row) for row in reader),
                                     content_type="text/csv")
    content = 'attachment; filename="' + experi_name + '.csv"'
    response['Content-Disposition'] = content
    return response
