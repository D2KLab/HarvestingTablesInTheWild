import os
import csv
import scrapy
from core.parsing.utils import get_parser_from_url


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
        else:
            raise Exception(
                'Need to either specify URL_STRING or URL_FILE')

        if not self.urls:
            raise Exception('No URLs found from provided resource')

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page_title = response.css('title::text').getall()[0]
        parser = get_parser_from_url(response.url)

        for table in parser.get_tables(response):
            try:
                yield parser.parse_table(table, url=response.url, page_title=page_title)
            # pylint: disable=broad-except
            except Exception as e:
                self.logger.error("Failed to parse table", e)
