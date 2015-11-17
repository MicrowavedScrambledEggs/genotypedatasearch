from django.shortcuts import render
from django.http import HttpResponse
import experimentlist.listretriever

from .models import Experiment


def index(request):
    """ For displaying the web page at the experimentlist index

    Updates the list of experiments, then prints out the list
    with field name headers
    :param request:
    :return: Response of printing the list of experiments
    """
    experimentlist.listretriever.retrieve_list(
        "http://10.1.8.167:8000/report/experiment/csv/"
    )
    field_names = Experiment.field_names
    output = [', '.join(field_names)]
    experiment_list = Experiment.objects.all()

    for experiment in experiment_list:
        attributes = (
            experiment.name, experiment.primary_investigator,
            experiment.date_created.strftime('%d.%m.%Y  %H:%M'),
            experiment.data_source,
        )
        output.extend(',  '.join(attributes))
    return HttpResponse('\n'.join(output))
