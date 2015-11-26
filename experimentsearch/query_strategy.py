from .models import Experiment, DataSource
from datetime import datetime


class AbstractQueryStrategy:

    def create_model(self, row):
        raise NotImplementedError("Concrete QueryStrategy missing this method")


class ExperimentQueryStrategy(AbstractQueryStrategy):

    file_name = "experi_list.csv"
    data_source_url = "data_source/?name="
    download_url = "download/"

    def create_model(self, row):
        # Creates and returns an experiment model from the values in the row
        name = row['name']
        who = row['pi']
        when = self._string_to_datetime(row['createddate'])
        ds = self.data_source_url + name.replace(" ", "+")
        dl = self.download_url + name.replace(" ", "+") + "/"
        return Experiment(
            name=name, primary_investigator=who, date_created=when,
            download_link=dl, data_source=ds,
        )

    def _string_to_datetime(self, date_string):
        """
        createddate field values in the database have a colon in the UTC info,
        preventing a simple call of just strptime(). Removes colon in UTC info
        so can create a datetime from strptime
        :param date_string: Date string from createddate field
        :return: datetime from processed date string
        """
        # removing the colon from the UTC info (the last colon)
        split_at_colon = date_string.split(":")
        front_rebuild = ":".join(split_at_colon[:-1])
        formatable_time = ''.join([front_rebuild, split_at_colon[-1]])

        return datetime.strptime(formatable_time, "%Y-%m-%d %X.%f%z")


class DataSourceQueryStrategy(AbstractQueryStrategy):

    file_name = "ds.csv"

    def create_model(self, row):
        # Creates a models.DataSource from the values in the given row
        supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
        return DataSource(
            name=row['name'], is_active=row['is_active'], source=row['source'],
            supplier=row['supplier'], supply_date=supplieddate,
        )
