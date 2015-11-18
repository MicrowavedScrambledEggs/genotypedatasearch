from django.shortcuts import render
from django.http import HttpResponse
import experimentlist.listretriever

from .models import Experiment


def index(request):
    """ For displaying the web page at the experimentlist index

    Updates the list of experiments, then displays the list
    according to the experimentlist/index.html template
    :param request:
    :return: Response from renderer
    """
    experimentlist.listretriever.retrieve_list(
        "http://10.1.8.167:8000/report/experiment/csv/"
    )
    experiment_list = Experiment.objects.all()
    return render(
        request, 'experimentlist/index.html',
        {'experiment_list': experiment_list}
    )


def search(request, search_term):
    search_list = Experiment.objects.filter(name=search_term)
    field_names = Experiment.field_names
    context = {
        'field_names': field_names, 'search_list': search_list,
    }
    return render(request, 'experimentlist/search.html', context)
