from django.shortcuts import render
from django.http import HttpResponse
import experimentlist.listretriever

from .models import Experiment


def index(request):
    experimentlist.listretriever.retrieve_list(
        "http://10.1.8.167:8000/report/experiment/csv/"
    )
    header = "Name,  Primary Investigator,  Date Created, Data Source"
    experiment_list = Experiment.objects.all()
    output = []
    for experiment in experiment_list:
        attributes = (
            experiment.name, experiment.primary_investigator,
            experiment.date_created.strftime('%d.%m.%Y  %H:%M'),
            experiment.data_source,
        )
        output.extend(',  '.join(attributes))
    return HttpResponse('\n'.join(output))