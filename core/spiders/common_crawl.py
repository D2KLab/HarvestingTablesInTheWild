import scrapy
from core.parsing.utils import get_parser_from_url, get_url_list_from_environment, get_title_from_text
from core.searching.common_crawl_search import CommonCrawlSearch

class CommonCrawlTableParserSpider(scrapy.Spider):
    name = "common_crawl_table_parser"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        urls = get_url_list_from_environment()

        if urls is None:
            raise Exception(
                'Need to either specify URL_STRING or URL_FILE')
        
        self.urls = urls

        if not self.urls:
            raise Exception('No URLs found from provided resource')

        self.common_crawl = CommonCrawlSearch()
        self.logger.info("Initialized common crawl object")
    
    #TODO: Look at custom item pipeline for extracting table?
    #https://docs.scrapy.org/en/latest/topics/item-pipeline.html#writing-your-own-item-pipeline
    
    def start_requests(self):
        for url in self.urls:
            filename, html = self.common_crawl.get_html_from_common_crawl(url)

            if filename is None:
                self.logger.info("No capture was found for this url")
            else:
                # Put the code here
                continue

    def parse(self, response, **kwargs):
        parser = get_parser_from_url(response.url)
        page_title = get_title_from_text(response)
        
        for table in parser.get_tables(response):
            try:
                yield parser.parse_table(table, url=response.url, page_title=page_title)
            # pylint: disable=broad-except
            except Exception as e:
                self.logger.error("Failed to parse table", e)