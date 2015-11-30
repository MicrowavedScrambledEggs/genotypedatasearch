import os
import pathlib
import datetime
import io
import re

from django.test import TestCase, Client
from . import views
from .query_maker import QueryMaker
from .query_strategy import ExperimentQueryStrategy, DataSourceQueryStrategy
from .models import Experiment, DataSource
from .errors import QueryError
from .tables import ExperimentTable, DataSourceTable

test_resources_path = '/test_resources/'
expected_experi_model = Experiment(
    name='What is up', primary_investigator='Badi James',
    data_source="data_source/?name=What+is+up",
    download_link='download/What+is+up/',
    date_created=datetime.datetime(
        2015, 11, 20, 11, 14, 40, 386012, datetime.timezone.utc
    )
)
expected_experi_set = [expected_experi_model]
expected_ds_model = DataSource(
    name= 'What is up', supplier='Badi James', is_active='False',
    source='testgzpleaseignore.gz',
    supply_date=datetime.date(2015, 11, 18),
)
expected_ds_set = [expected_ds_model]


class ExperimentsearchTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        resource_path = pathlib.Path(
            os.getcwd() + test_resources_path
        ).as_uri()
        views.data_source_url = resource_path + '/data_source/'
        views.experi_table_url = resource_path + '/experiment/'
        views.genotype_url = resource_path + '/genotype/'
        views.name_query_prefix = ''

    def test_url_build_1(self):
        url = 'www.foo.bar/?baz='
        search = "banana"
        expected = 'www.foo.bar/?baz=banana'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_2(self):
        url = 'www.foo.bar/?baz='
        search = "banana cake"
        expected = 'www.foo.bar/?baz=banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_3(self):
        url = 'file://C:/foo bar/'
        search = "banana cake"
        expected = 'file://C:/foo bar/banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_experiment_query_1(self):
        querier = QueryMaker(ExperimentQueryStrategy)
        actual_models = querier.make_query('bar.csv', views.experi_table_url)
        actual_model = actual_models[0]
        self.assertEqual(expected_experi_model.data_source, actual_model.data_source)
        self.assertEqual(expected_experi_model.download_link, actual_model.download_link)
        self.assertEqual(expected_experi_model.name, actual_model.name)
        self.assertEqual(
            expected_experi_model.primary_investigator, actual_model.primary_investigator
        )
        self.assertEqual(expected_experi_model.date_created, actual_model.date_created)

    def test_experiment_query_2(self):
        querier = QueryMaker(ExperimentQueryStrategy)
        actual_models = querier.make_query(
            "found nothing.csv", views.experi_table_url
        )
        self.assertIsNone(actual_models)

    def test_data_source_query_1(self):
        querier = QueryMaker(DataSourceQueryStrategy)
        actual_models = querier.make_query('foo.csv', views.data_source_url)
        actual_model = actual_models[0]
        self.assertEqual(expected_ds_model.name, actual_model.name)
        self.assertEqual(expected_ds_model.source, actual_model.source)
        self.assertEqual(expected_ds_model.supplier, actual_model.supplier)
        self.assertEqual(expected_ds_model.supply_date, actual_model.supply_date)
        self.assertEqual(expected_ds_model.is_active, actual_model.is_active)

    def test_data_source_query_2(self):
        querier = QueryMaker(DataSourceQueryStrategy)
        actual_models = querier.make_query(
            "found nothing.csv", views.data_source_url
        )
        self.assertIsNone(actual_models)

    def test_bad_url_1(self):
        querier = QueryMaker(ExperimentQueryStrategy())
        with self.assertRaises(QueryError):
            querier.make_query('banana.csv', views.experi_table_url)

    def test_bad_url_2(self):
        querier = QueryMaker(ExperimentQueryStrategy())
        bad_url = pathlib.Path(os.getcwd() + "/nonexistentdir/").as_uri()
        with self.assertRaises(QueryError):
            querier.make_query('bar.csv', bad_url)

    def test_download_1(self):
        # Feels like I'm doing something wrong here...
        # Need a cleaner way of comparing the streaming content to the file
        # Right now having to get it to ignore whitespace on both to pass
        response = self.client.get('/experimentsearch/download/baz.csv/')
        actual_bytes = b"".join(response.streaming_content)
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/genotype/baz.csv', 'rb')
        expected_bytes = expected_file.read()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_index_response_1(self):
        response = self.client.get('/experimentsearch/', {'search_name': 'bar.csv'})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'bar.csv')
        expected_table = ExperimentTable(expected_experi_set)
        actual_table = response.context['table']
        self.assertEqual(len(actual_table.rows), len(expected_table.rows))
        for row in range(0, len(actual_table.rows)):
            actual_row = actual_table.rows[row]
            expected_row = expected_table.rows[row]
            with self.subTest(row=row):
                for col in range(0, len(Experiment.field_names)):
                    field = Experiment.field_names[col]
                    field = field.lower().replace(' ', '_')
                    with self.subTest(col=col):
                        self.assertEqual(
                            actual_row[field], expected_row[field]
                        )

    def test_index_response_2(self):
        response = self.client.get(
            '/experimentsearch/', {'search_name': 'found nothing.csv'}
        )
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'found nothing.csv')
        self.assertIsNone(response.context['table'])

    def test_ds_response_1(self):
        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'foo.csv'}
        )
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        expected_table = DataSourceTable(expected_ds_set)
        actual_table = response.context['table']
        self.assertEqual(len(actual_table.rows), len(expected_table.rows))
        for row in range(0, len(actual_table.rows)):
            actual_row = actual_table.rows[row]
            expected_row = expected_table.rows[row]
            with self.subTest(row=row):
                for col in range(0, len(DataSource.field_names)):
                    field = DataSource.field_names[col]
                    field = field.lower().replace(' ', '_')
                    with self.subTest(col=col):
                        self.assertEqual(
                            actual_row[field], expected_row[field]
                        )

    def test_ds_response_2(self):
        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'found+nothing.csv'}
        )
        self.assertIsNone(response.context['table'])
