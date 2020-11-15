import scrapy

from core.parsing.utils import get_parser_from_url, get_url_list_from_environment, get_title_from_text


class CommonCrawlTableParserSpider(scrapy.Spider):
    name = "common_crawl_table_parser"
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = get_url_list_from_environment()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse, meta={'explicit': True})

    def parse(self, response, **kwargs):
        parser = get_parser_from_url(response.url)
        page_title = get_title_from_text(response)

        for table in parser.get_tables(response):
            try:
                yield parser.parse_table(table, url=response.url, page_title=page_title)
            # pylint: disable=broad-except
            except Exception as e:
                self.logger.error("Failed to parse table", e)
