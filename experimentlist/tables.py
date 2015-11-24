import django_tables2 as tables
from .models import Experiment, DataSource


class ExperimentTable(tables.Table):
    download_link = tables.TemplateColumn('<a href="{{record.download_link}}">Download</a>')
    data_source = tables.TemplateColumn('<a class="dslinks" href="{{record.data_source}}">Link</a>')

    class Meta:
        model = Experiment
        exclude = ("id", )
        attrs = {"class": "paleblue"}


class DataSourceTable(tables.Table):
    class Meta:
        model = DataSource
        exclude = ("id", )
        attrs = {"class": "paleblue"}
