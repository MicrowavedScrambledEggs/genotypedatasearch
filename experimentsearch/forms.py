import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Experiment


class SearchTypeSelect(forms.Form):
    parameters = (
        (Experiment.field_names[0], Experiment.field_names[0]),
        (Experiment.field_names[1], Experiment.field_names[1]),
        (Experiment.field_names[2], Experiment.field_names[2])
    )
    search_by = forms.ChoiceField(
        parameters, label='Search by', required=False,
        widget=forms.Select(attrs={"onChange": 'this.form.submit()'})
    )


class NameSearchForm(forms.Form):
    search_name = forms.CharField(
        max_length=200, label='',
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class PISearchForm(forms.Form):
    search_pi = forms.CharField(
        max_length=200, label='',
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class DateSearchForm(forms.Form):
    current_year = datetime.datetime.now().year
    years = []
    for year in range(2013, current_year+1):
        years.append(year)
    search_date = forms.DateTimeField(
        label='', widget=SelectDateWidget(years=years),
    )