import os

from lazy import lazy
from prometheus_client import Counter, Summary, CollectorRegistry, push_to_gateway


class Metrics:
    def __init__(self):
        self.prometheus_gw = os.environ.get('PROMETHEUS_PUSH_GW')
        if not self.prometheus_gw:
            raise Exception('PROMETHEUS_PUSH_GW not defined')
        self.registry = CollectorRegistry()

    def push(self, job_name):
        push_to_gateway(
            self.prometheus_gw,
            registry=self.registry,
            job=job_name,
        )

    @lazy
    def table_scraping_invalid_table_errors_total(self):
        return Counter(
            'table_scraping_invalid_table_errors_total',
            'Count of failed table parsing attempts',
            registry=self.registry
        )

    @lazy
    def table_scraping_unknown_errors_total(self):
        return Counter(
            'table_scraping_unknown_errors_total',
            'Count of unknown errors received during parsing',
            registry=self.registry
        )

    @lazy
    def table_scraping_tables_in_page_total(self):
        return Summary(
            'table_scraping_tables_in_page_total',
            'Amount of tables found in a single HTML page',
            registry=self.registry
        )

    @lazy
    def table_scraping_request_seconds(self):
        return Summary(
            'table_scraping_request_seconds',
            'Request time to the Common Crawl Corpus',
            labelnames=['spider'],
            registry=self.registry
        )

    @lazy
    def table_scraping_cc_request_seconds(self):
        return self.table_scraping_request_seconds.labels('common_crawl')


metrics = Metrics()
