import os
import json
from abc import ABC, abstractmethod
from arango import ArangoClient


class TableCollector(ABC):
    '''
    Database system agnostic Abstract Base Class that describes methods
    required for collecting ingested data
    '''
    @abstractmethod
    def append(self, data) -> None:
        pass


class ArangoTableCollector(TableCollector):
    __COLLECTION = 'parsed_tables'
    __DATABASE = '_system'

    def __init__(self):
        arango_host = os.environ.get('ARANGO_HOST')
        if not arango_host:
            raise Exception('ARANGO_HOST not defined')

        raw_credentials = os.environ.get('ARANGODB_CREDENTIALS', '{}')
        credentials = json.loads(raw_credentials)

        self.client = ArangoClient(hosts=arango_host)
        self.db = self.client.db(
            ArangoTableCollector.__DATABASE, **credentials)

    def append(self, data):
        tables = self.db.create_collection(ArangoTableCollector.__COLLECTION)
        tables.insert(data)
