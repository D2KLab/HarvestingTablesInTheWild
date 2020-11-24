#!/bin/sh

set -e

tmp_file="$(mktemp).json"
URL_FILE=data/test-urls.txt scrapy crawl web -O "$tmp_file"
scripts/validate_schema.py data/schema.json "$tmp_file"
rm -f "$tmp_file"
