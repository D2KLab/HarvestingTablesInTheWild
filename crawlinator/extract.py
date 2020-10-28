#!/usr/bin/env python3

import logging
from typing import List, Dict
import json
from datetime import datetime

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


def clean_whitespace(text: str) -> str:
    text = text.replace('\t', ' ') # replace tabs with withspace
    text = text.strip() # remove leading / trailing whitespace
    return text


class FetchTable(scrapy.Spider):
    """
    Fetches a table using scrapy crawling service
    """

    name = "fetchTable"

    custom_settings = {
        'LOG_LEVEL': logging.ERROR,
    }

    def __init__(self, url_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not url_string:
            raise ValueError('No url provided')

        self.urls = url_string.split(',')
        self.type=type

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page_title = response.css('title::text').getall()[0]
        tables = response.css('table')

        for table in tables:
            # empty object in which we will build our parsed table
            obj = {}

            # Add header row
            header_row = table.css('table thead tr')
            header_columns = header_row.css('th ::text')
            header_values = header_columns.getall()
            for k in range(len(header_values)):
                # clean headers
                header_values[k] = clean_whitespace(header_values[k])

                # create empty lists for each header element
                # so we can later easily .append to it
                obj[header_values[k]] = []

            # Add data rows
            body_rows = table.css('table tbody tr')
            for row in body_rows:
                columns = row.css('td ::text')
                column_values = columns.getall()

                # append each value of this column to the correct object element
                for k in range(len(column_values)):
                    obj[header_values[k]].append(
                        clean_whitespace(column_values[k]),
                        )

            # Save table object
            store_table(response.url, page_title, obj)

def store_table(url: str, page_title: str, table: Dict[str, List[str]]):
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


def crawl_urls(urls: List[str]):
    process = CrawlerProcess(get_project_settings())
    process.crawl(FetchTable, url_string=",".join(urls))
    process.start()

def craw_cc_urls(urls: List[str]):
    # TODO: implement crawling pages from CommonCrawls dataset
    # https://commoncrawl.org/the-data/get-started/
    pass
