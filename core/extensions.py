from scrapy.extensions.corestats import CoreStats

from monitoring.metrics import metrics


class PrometheusStatsExtension(CoreStats):
    def spider_closed(self, spider, reason):
        '''
        Some potentially interesting metrics inherited from CoreStats:
            start_time
            finish_time
            finish_reason
            item_scraped_count
            elapsed_time_seconds
            response_received_count
        These can be accessed using: self.stats.get_value('<metric>')
        '''
        super().spider_closed(spider, reason)
        metrics.push(spider.name)
