#!/usr/bin/env python3

from enum import Enum
import json
from datetime import datetime

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class XPathSelector(str, Enum):
    TABLE="//table"
    TABLE_ROW=".//tr"
    TABLE_HEADER_ROW=".//th"
    TABLE_DATA_ROW=".//td"
    TEXT="text()"


def append_row_values(row: scrapy.selector.unified.SelectorList, path_selector: str) -> str:
    row_list = row.xpath(path_selector).getall()
    return ", ".join(row_list)


class FetchTable(scrapy.Spider):
    """
    Fetches a table using scrapy crawling service
    """

    name = "fetchTable"

    def __init__(self, url_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not url_string:
            raise ValueError('No url provided')

        self.urls = url_string.split(',')
        self.type=type

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table_list = []
        print(XPathSelector.TABLE)
        tables = response.xpath(XPathSelector.TABLE)

        for table in tables:
            table_rows = []

            rows = table.xpath(XPathSelector.TABLE_ROW)
            print(type(rows))
            # Add header row
            table_rows.append(
                append_row_values(rows, f"{XPathSelector.TABLE_HEADER_ROW}/{XPathSelector.TEXT}"))

            # Add data rows
            for row in rows:
                table_rows.append(
                    append_row_values(row, f"{XPathSelector.TABLE_DATA_ROW}/{XPathSelector.TEXT}"))

            table_list.append(table_rows)

        print(table_list)
def store_table(url, page_title, table):
    """Stores a table with given metadata and content in JSON file"""
    obj = {
        'url': url,
        'timestamp': datetime.now().isoformat(), # ISO 8601
        'page_title': page_title,
        'table': table,
    }

    # Example table:

    # COUNTRY, SIZE
    # Finland  5.5
    # Germany  80
    # Norway
    # USA      506

    # table = {
    #   "Country" : ["Finland","Germany","Norway", "USA"],
    #   "Size": ["5.5", "80", "", "506"],
    # }

    # TODO: store this as JSON file
    print(json.dumps(obj, indent=2))


def crawl_urls(urls: List[str]) -> List:
    process = CrawlerProcess(get_project_settings())
    process.crawl(FetchTable, url_string=",".join(urls))
    process.start()

