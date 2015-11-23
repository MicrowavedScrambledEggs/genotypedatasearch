from django.shortcuts import render
from django.http import HttpResponse

from .models import Experiment
from .forms import SearchForm
from .listretriever import search_experiments


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
        search_term = request.GET['search_field']
        search_list = search_experiments(search_term)
        field_names = Experiment.field_names
        context = {
            'field_names': field_names, 'search_list': search_list,
            'search_form': form, 'search_term': search_term,
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
