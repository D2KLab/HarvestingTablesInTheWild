from datetime import datetime
import traceback
import os

import scrapy

from core.parsing.utils import get_url_list_from_environment, get_title_from_text, get_term_set, get_text_before, get_text_after
from core.parsing.parsers import get_parser_from_url
from core.items import CoreDataItem
from core.crawling.strategy import CrawlingStrategy


class TableParserSpider(scrapy.Spider):
    name = 'web'
    crawling_strategy = CrawlingStrategy(
        follow_links=(os.environ.get('FOLLOW_LINKS') == "true"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = get_url_list_from_environment()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # the following items are specific to the page,
        # so we only retrieve them once here
        page_title = get_title_from_text(response)
        parser = get_parser_from_url(response.url)
        timestamp = datetime.now().isoformat()
        table_number = 0
        term_set = get_term_set(response)

        for table in parser.get_tables(response):
            table_number += 1
            try:
                core_table = parser.parse_table(table)
            # pylint: disable=broad-except
            except Exception as e:
                self.logger.error("Failed to parse table on %s: %s", response.url, e)
                traceback.print_exc()
                continue

            yield CoreDataItem(
                relation=core_table.table,
                headers=core_table.headers,
                hasHeader=bool(core_table.headers),
                headerPosition=core_table.header_position,
                tableNum=table_number,
                tableType=core_table.table_type,
                termSet=term_set,
                title=core_table.title,
                pageTitle=page_title,
                url=response.url,
                timestamp=timestamp,
                markup=table.get(),
                textBeforeTable=get_text_before(table),
                textAfterTable=get_text_after(table),
                s3Link="",
                recordOffset=0,
                recordEndOffset=0,
            )

        # also crawl all links in the webpage, according to crawl strategy
        links = CrawlingStrategy.get_links_to_follow(response.url, response.css('body'))
        yield from response.follow_all(links, callback=self.parse)
