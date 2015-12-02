from .query_maker import QueryMaker
from .query_strategy import ExperimentUpdate
from .views import experi_table_url
from .errors import QueryError


def sync_with_genotype_db():
    syncer = QueryMaker(ExperimentUpdate)
    try:
        # syncer.make_query('', experi_table_url)
        # For testing
        syncer.make_query('', 'file:///C:/Users/cfpbtj/PycharmProjects/genotypedatasearch/experi_list.csv')
    except QueryError:
        print("Syncing Failed")