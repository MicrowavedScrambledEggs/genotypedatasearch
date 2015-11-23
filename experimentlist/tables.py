import django_tables2 as tables
from .models import Experiment


class ExperimentTable(tables.Table):
    download_link = tables.TemplateColumn('<a href="{{record.download_link}}">Download</a>')

    class Meta:
        model = Experiment
        exclude = ("id", )
        attrs = {"class": "paleblue"}


