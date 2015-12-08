import pathlib, os

from .query_maker import QueryMaker
from .query_strategy import ExperimentUpdate
from .views import experi_table_url
from .errors import QueryError

# sync_url = experi_table_url
# When genotype database down:
# sync_url = resource_path = pathlib.Path(
#             os.getcwd() + "/experi_list.csv"
#         ).as_uri()
sync_url = 'file:///C:/Users/cfpbtj/PycharmProjects/genotypedatasearch/experi_list.csv'


def sync_with_genotype_db():
    print("synching with " + sync_url)
    syncer = QueryMaker(ExperimentUpdate)
    try:
        syncer.make_query('', sync_url)
        print("syncing finished")
    except QueryError as e:
        print("Syncing Failed because:\n" + str(e))