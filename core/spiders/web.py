from datetime import datetime
import traceback

import scrapy

from core.parsing.utils import get_url_list_from_environment, get_title_from_text, get_term_set
from core.parsing.parsers import get_parser_from_url
from core.parsing.exceptions import InvalidTableException
from core.items import CoreDataItem

from monitoring.metrics import metrics


class TableParserSpider(scrapy.Spider):
    name = 'web'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = get_url_list_from_environment()

    @staticmethod
    def close(spider, reason):
        metrics.push(spider.name)

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
                    textBeforeTable="",  # TODO
                    textAfterTable="",  # TODO
                    s3Link="",  # TODO
                    recordOffset=0,
                    recordEndOffset=0,
                )
            except InvalidTableException:
                metrics.table_scraping_invalid_table_errors_total.inc()
            # pylint: disable=broad-except
            except Exception as e:
                metrics.table_scraping_unknown_errors_total.inc()
                self.logger.error(
                    "Failed to parse table on %s: %s", response.url, e)
                traceback.print_exc()
        metrics.table_scraping_tables_in_page_total.observe(table_number)
