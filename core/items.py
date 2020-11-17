# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
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

@dataclass
class CoreDataItem: # pylint: disable=too-many-instance-attributes
    """
    External data format which will be used for exporting
    Contains all information and metadata about the table and webpage
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
    termSet: List[int]
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
