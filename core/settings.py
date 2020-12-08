import os

# Scrapy settings for core project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'core'

SPIDER_MODULES = ['core.spiders']
NEWSPIDER_MODULE = 'core.spiders'

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'core (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Use a priority queue that works well for multi-domain crawls
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Increase threadpool size for faster DNS resolution
REACTOR_THREADPOOL_MAXSIZE = 32

# Disable retries for faster crawls
RETRY_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_crawl_once.CrawlOnceMiddleware': 100,
    'core.middlewares.CoreSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_crawl_once.CrawlOnceMiddleware': 50,
    'core.middlewares.CoreDownloaderMiddleware': 543,
}

CRAWL_ONCE_ENABLED = (os.environ.get('CRAWL_ONCE', 'false') == 'true')

# from scrapy.downloadermiddlewares import DownloaderMiddleware

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
   'scrapy_kafka_export.KafkaItemExporterExtension': 1,
}

# Kafka Exporter configuration, see https://github.com/TeamHG-Memex/scrapy-kafka-export
KAFKA_EXPORT_ENABLED = (os.environ.get('KAFKA_EXPORT', 'false') == 'true')
KAFKA_BROKERS = [
    'kafka:9092', # see docker-compose.yml
]
KAFKA_TOPIC = 'tablecollector'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'core.pipelines.CorePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
