import cdx_toolkit
from scrapy.selector import Selector

import sys
sys.path.append("/home/rohit/Documents/HarvestingTablesInTheWild")
from core.parsing.utils import get_parser_from_url, get_title_from_text

class CommonCrawlPageFetch:
    @staticmethod
    def parse_table_from_Html(html: str, parser):
        print(get_title_from_text(html))
        print(Selector(text=html).css("title ::text").getall())


class CommonCrawlSearch:
    def __init__(self, url):
        cdx = cdx_toolkit.CDXFetcher(source='cc')
        parser = get_parser_from_url(url)
        for search_result in cdx.iter(url, limit=1):
            search_result_data = search_result.data
            if search_result_data['status'] == '200':
                CommonCrawlPageFetch.parse_table_from_Html(search_result.content, parser)


CommonCrawlSearch("en.wikipedia.org/wiki/Finland")