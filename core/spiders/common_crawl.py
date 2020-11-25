import scrapy

from core.spiders.web import TableParserSpider


class CommonCrawlTableParserSpider(TableParserSpider):
    name = 'common_crawl_table_parser'
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse, meta={'explicit': True})
