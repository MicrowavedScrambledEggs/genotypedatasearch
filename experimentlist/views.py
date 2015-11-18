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
    field_names = Experiment.field_names
    experiment_list = Experiment.objects.all()
    context = {
        'field_names': field_names, 'experiment_list': experiment_list
    }
    return render(request, 'experimentlist/index.html', context)
