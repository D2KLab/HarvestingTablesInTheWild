# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, asdict
from typing import List

@dataclass
class CoreTableItem:
    """
    Internal data format (subject to change)
    Contains information strictly related to this specific table
    """
    table: dict
    title: str
    header_position: str
    table_type: str
    markup: str
    headers: List[str]
    orientation: str
    nb_columns: int
    nb_rows: int

@dataclass
class CoreDataItem: # pylint: disable=too-many-instance-attributes
    """
    External data format which will be used for exporting
    Contains all information and metadata about the table and webpage
    Format according to data/schema.json
    """

    # pylint: disable=invalid-name
    # these names are set so we comply with DWTC JSON attributes

    # data attributes from DWTC:
    hasHeader: bool
    recordEndOffset: int
    recordOffset: int
    relation: List[List[str]]
    s3Link: str
    tableNum: int
    termSet: List[str]
    title: str # table title / caption
    pageTitle: str
    url: str
    headerPosition: str # TODO: make this into an enum or similar
    tableType: str # TODO: make this into an enum or similar
    # custom attributes:
    markup: str # raw table html
    textBeforeTable: str
    textAfterTable: str
    headers: List[str]
    timestamp: str
    tableOrientation: str
    language: str
    nbColumns: int
    nbRows: int
    referrer: str

    # expose a dynamic getter for this item
    # required for kafka-exporter
    def get(self, key, default_value=None):
       return asdict(self).get(key, default_value)

   # method that makes this item comparable
   # required for unit tests
    def __eq__(self, other):
        return asdict(self) == asdict(other)
