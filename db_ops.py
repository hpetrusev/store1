import json
from abc import abstractmethod
from dataclasses import dataclass
import typing
from enum import Enum


class Datasets(Enum):
    prices = "prices"
    offers = "offers"


@dataclass
class Filtering:
    filter_by: str
    filter_value: typing.List[typing.Any]


class DatabaseBase:
    @abstractmethod
    def get(self, data, filters: typing.List[Filtering] = None):
        pass


class JsonDatabase(DatabaseBase):
    metadata = {"prices": "pricedb.json", "offers": "offerdb.json"}
    data = {}

    def load(self, data):

        if data in self.metadata.keys():
            pass
        else:
            raise Exception(f"only {self.metadata.keys()} available!")

        with open(self.metadata[data], "r") as f:
            data_requested = json.load(f)

        return data_requested

    def get(self, data, filters: typing.List[Filtering] = None):
        if filters is None:
            filters = []
        """
        JsonDatabase implementation of the get method
        
        :param data: data interested in
        :param filters: list of filtering to be applied
        :return: list of data of interest
        """

        if data not in self.data.keys():
            self.data[data] = self.load(data)

        if len(filters) == 0:
            return self.data[data]
        else:
            return_values_filtered = list(
                filter(
                    lambda element: all(
                        (element[f.filter_by] in f.filter_value for f in filters)
                    ),
                    self.data[data],
                )
            )
            return return_values_filtered


def get_database(type_of_db) -> DatabaseBase:
    """
    Currently its only the Json file formatter, but it can easily be a database
    or storage format of diff type, in which case there would be a config setup to switch between
    :return: database connector
    """
    available_databases = {"jsondb": JsonDatabase}

    return available_databases[type_of_db]()
