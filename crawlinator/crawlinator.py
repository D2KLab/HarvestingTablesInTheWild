#!/usr/bin/env python3

import argparse
import sys

from extract import crawl_urls

def main():
    parser = argparse.ArgumentParser(prog='crawlinator.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="""Fetches and extracts table from HTML pages. Example URLs:
                                     https://www.ecdc.europa.eu/en/cases-2019-ncov-eueea
                                     https://www.w3schools.com/html/html_tables.asp
                                     """)
    parser.add_argument('url', nargs='*', action='append')
    args = parser.parse_args()
    if len(args.url[0]) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
    crawl_urls(args.url[0])


if __name__ == "__main__":
    main()
