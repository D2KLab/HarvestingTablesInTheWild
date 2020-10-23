import os
import scrapy
import numpy as np
from scrapy.http import Request


class TableParserSpider(scrapy.Spider):
    name = 'table_parser'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url_file = os.environ.get('URL_FILE')
        if not url_file:
            raise Exception('URL_FILE environment variable must be set')
        self.urls = np.loadtxt(url_file, dtype=np.str)

    def parse(self, response, **kwargs):
        # TODO
        pass

    def start_requests(self):
        for url in self.urls:
            yield Request(url, self.parse)
