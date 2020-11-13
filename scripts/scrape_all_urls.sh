#!/bin/bash

URL_STRING=$(cat data/* | tr '\n' ',') scrapy crawl common_crawl_table_parser
