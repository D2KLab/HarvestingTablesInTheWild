import cdx_toolkit
from scrapy.selector import Selector

import sys
sys.path.append("/home/rohit/Documents/HarvestingTablesInTheWild")

from core.parsing.utils import get_parser_from_url, get_title_from_text


class CommonCrawlTable:
    @staticmethod
    def parse_table_from_raw_Html(html, page_title, url, parser):
        scrapy_response = Selector(text=html)
        for table in parser.get_tables(scrapy_response):
            try:
                yield parser.parse_table(table, url=url, page_title=page_title)
            # pylint: disable=broad-except
            except Exception as e:
                print(e)


class CommonCrawlSearch:
    def __init__(self, limit=1, index_start_month="202008", index_end_month="202009"):
        self.limit = limit
        self.start_month = index_start_month
        self.end_month = index_end_month
        self.cdx = cdx_toolkit.CDXFetcher(source='cc')

    def search_common_crawl(self, cc_url=""):        
        for search_result in self.cdx.iter(cc_url, limit=self.limit, from_ts=self.start_month, to=self.end_month):
                search_result_data = search_result.data
                if search_result_data['status'] == '200':
                    return search_result_data['url'], search_result.content
        return None, ""

    def generate_table(self, url, html):
        parser= get_parser_from_url(url)
        page_title = get_title_from_text(html)
        CommonCrawlTable.parse_table_from_raw_Html(html, page_title, url, parser)

    def get_tables_from_common_crawl(self):
        url, raw_html = self.search_common_crawl()
        if url is not None:
            self.generate_table(url, raw_html)
        else:
            print("No URL was found for this ")

#CommonCrawlSearch("https://en.wikipedia.org/wiki/Chhapra")


with open ("/home/rohit/Desktop/a.html", "r") as myfile:
    data=myfile.read()

parse_table_from_Html(data, "https://en.wikipedia.org/wiki/Chhapra")