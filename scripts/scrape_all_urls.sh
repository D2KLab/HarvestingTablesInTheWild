#!/bin/bash

URL_STRING=$(cat data/* | tr '\n' ',') scrapy crawl table_parser
