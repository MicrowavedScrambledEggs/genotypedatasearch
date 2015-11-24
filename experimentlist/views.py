from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import RequestConfig

from .models import Experiment
from .forms import SearchForm
from .experiment_query_maker import query_experiments
from .tables import ExperimentTable, DataSourceTable
from .ds_query_maker import query_data_source


def index(request):
    """
    Renders the search page according to the index.html template, with a
    form.SearchForm as the search form.

    If the search form has any GET data, retrieves models.Experiment that
    match the GET data to populate a table

    :param request:
    :return:
    """
    if request.method == 'GET' and 'search_field' in request.GET:
        form = SearchForm(request.GET)
        search_term = request.GET['search_field'].strip()
        search_list = query_experiments(search_term)
        if search_list is None:
            table = None
        else:
            table = ExperimentTable(search_list)
            RequestConfig(request, paginate={"per_page": 25}).configure(table)
        context = {
            'search_form': form, 'search_term': search_term,
            'table': table,
        }
        return render(
            request, 'experimentlist/index.html', context
        )
    else:
        return render(
            request, 'experimentlist/index.html',
            {'search_form': SearchForm()}
        )


def search(request, search_term):
    """
    Renders the search page according to the search.html template,
    that is populating a table wit models.Experiments who's names
    match the search_term parameter.
    Called when url "~/experimentlist/<someExperimentName>/" requested

    No longer used as using forms, but kept around for testing

    :param request:
    :param search_term: Name models.Experiment need to match to be in table
    :return:
    """
    search_list = Experiment.objects.filter(name=search_term)
    field_names = Experiment.field_names
    context = {
        'field_names': field_names, 'search_list': search_list,
    }
    return render(request, 'experimentlist/search.html', context)


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
            ds_list = query_data_source(ds_name)
            if ds_list is None:
                table = None
            else:
                table = DataSourceTable(ds_list)
                RequestConfig(request, paginate={"per_page": 25}).configure(table)
            return render(
                request, 'experimentlist/datasource.html',
                {'table': table, 'ds_name': ds_name, 'from': from_page}
            )
    return render(request, 'experimentlist/datasource.html', {})
