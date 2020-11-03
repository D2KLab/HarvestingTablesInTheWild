# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class CoreTableItem:
    # define the fields for your item here like:
    page_title: str
    timestamp: str
    table: dict
    url: str
