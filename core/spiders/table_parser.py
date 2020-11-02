import os
from datetime import datetime
from typing import Dict
import csv

import scrapy
#from scrapy.http import Request

def clean_whitespace(text: str) -> str:
    text = text.replace('\t', ' ') # replace tabs with withspace
    text = text.strip() # remove leading / trailing whitespace
    return text

class TableParserSpider(scrapy.Spider):
    name = 'table_parser'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        url_string = os.environ.get('URL_STRING')
        url_file = os.environ.get('URL_FILE')

        if url_string:
            self.urls = url_string.split(',')
        elif url_file:
            with open(url_file, 'r') as fd:
                self.urls = []
                for row in csv.reader(fd):
                    self.urls.append(row[0])

        if not self.urls:
            raise Exception('Error: Need to either specify URL_STRING or URL_FILE')

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_single_table(self, table) -> Dict:
        try:
            # empty object in which we will build our parsed table
            obj = {}

            # Add header row
            header_columns = table.css('tr th ::text')
            header_values = header_columns.getall()
            for k, _ in enumerate(header_values):
                # clean headers
                header_values[k] = clean_whitespace(header_values[k])

                # create empty lists for each header element
                # so we can later easily .append to it
                obj[header_values[k]] = []

            # Add data rows
            body_rows = table.css('tr')
            for row in body_rows:
                columns = row.css('td ::text')
                column_values = [x for x in columns.getall() if x == '' or clean_whitespace(x) != '']
                # append each value of this column to the correct object element
                for k, _ in enumerate(column_values):
                    obj[header_values[k]].append(
                        clean_whitespace(column_values[k]),
                        )
            # Return 'Scrapy item'
            return {
                'timestamp': datetime.now().isoformat(), # ISO 8601
                'table': obj,
            }
        except Exception as e:
               print(e)


    def parse(self, response, **kwargs):
        page_title = response.css('title::text').getall()[0]
        tables = response.css('table')

        for table in tables:
            obj = self.parse_single_table(table)
            if obj:
                obj['url'] = response.url
                obj['page_title'] = page_title
                yield obj
