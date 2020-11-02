import cdx_toolkit
import requests
from warcio.archiveiterator import ArchiveIterator

class CommonCrawlPageFetch:
    common_crawl_base_url = "https://commoncrawl.s3.amazonaws.com/"       

    def fetch_records(self, filename):
        url = f"{self.common_crawl_base_url}{filename}"
        resp = requests.get(url, stream=True)

        for record in ArchiveIterator(resp.raw, arc2warc=True):
            if record.rec_type == 'response':
                if record.http_headers.get_header('Content-Type') == 'text/html':
                    print(record.rec_headers.get_header('WARC-Target-URI'))
                    # For now printing the first 1000 characters
                    print(record.content_stream().read().decode('UTF-8', errors='ignore')[:1000])
                    print('')

class CommonCrawlSearch:
    def __init__(self, url):
        cdx = cdx_toolkit.CDXFetcher(source='cc')
        common_crawl_page_fetch_service = CommonCrawlPageFetch()

        for search_result in cdx.iter(url, limit=1):
            search_result_data = search_result.data
            if search_result_data['status'] == '200':
                common_crawl_page_fetch_service.fetch_records(search_result_data['filename'])


CommonCrawlSearch("en.wikipedia.org/wiki/Finland")