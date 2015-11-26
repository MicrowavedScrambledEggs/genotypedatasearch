import os
import pathlib

from django.test import TestCase, Client
from . import views

test_resources_path = '/test_resources/'


class ExperimentsearchTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        resource_path = pathlib.Path(os.getcwd()) + test_resources_path
        views.data_source_url = resource_path + 'data_source/'
        views.experi_table_url = resource_path + 'experiment/'
        views.genotype_url = resource_path + 'genotype/'

