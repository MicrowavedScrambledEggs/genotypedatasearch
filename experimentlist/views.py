from django.shortcuts import render
from django.http import HttpResponse

from .models import Experiment
from .forms import SearchForm
from .listretriever import retrieve_list, _create_experiment_models


def index(request):
    if request.method == 'GET' and 'search_field' in request.GET:
        form = SearchForm(request.GET)
        search_term = request.GET['search_field']
        # retrieve_list(
        #     "http://10.1.8.167:8000/report/experiment/csv/"
        # )
        Experiment.objects.all().delete()
        _create_experiment_models(open("experi_list.csv"))
        search_list = Experiment.objects.filter(name=search_term)
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
    search_list = Experiment.objects.filter(name=search_term)
    field_names = Experiment.field_names
    context = {
        'field_names': field_names, 'search_list': search_list,
    }
    return render(request, 'experimentlist/search.html', context)
