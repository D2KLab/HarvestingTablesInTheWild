import scrapy

from core.parsing.utils import get_parser_from_url, get_url_list_from_environment, get_title_from_text


class TableParserSpider(scrapy.Spider):
    name = 'table_parser'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = get_url_list_from_environment()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        page_title = get_title_from_text(response)
        parser = get_parser_from_url(response.url)

        for table in parser.get_tables(response):
            try:
                yield parser.parse_table(table, url=response.url, page_title=page_title)
            # pylint: disable=broad-except
            except Exception as e:
                self.logger.error("Failed to parse table", e)
