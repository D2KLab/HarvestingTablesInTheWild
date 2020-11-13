import cdx_toolkit
from scrapy.selector import Selector

#remove if not required
class CommonCrawlTableParser:
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
    def __init__(self, limit=1, index_start_month="202005", index_end_month="202006"):
        self.limit = limit
        self.start_month = index_start_month
        self.end_month = index_end_month
        self.cdx = cdx_toolkit.CDXFetcher(source='cc')

    def __search_common_crawl(self, cc_url=""):        
        for search_result in self.cdx.iter(cc_url, limit=self.limit, from_ts=self.start_month, to=self.end_month):
                search_result_data = search_result.data
                if search_result_data['status'] == '200':
                    return search_result_data['filename'], search_result.content
        return None, ""

    def get_html_from_common_crawl(self, url):
        return self.__search_common_crawl(url)