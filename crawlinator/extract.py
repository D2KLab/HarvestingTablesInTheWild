#!/usr/bin/env python3

from enum import Enum
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


process = CrawlerProcess(get_project_settings())
process.crawl(FetchTable, url_string="https://www.w3schools.com/html/html_tables.asp")
process.start()
