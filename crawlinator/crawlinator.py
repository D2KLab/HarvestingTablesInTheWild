#!/usr/bin/env python3

import argparse
import sys

from extract import crawl_urls

def main():
    parser = argparse.ArgumentParser(prog='crawlinator.py',
                                     description='Fetches and extracts table from HTML pages')
    parser.add_argument('url', nargs='*', action='append')
    args = parser.parse_args()
    if len(args.url[0]) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
    crawl_urls(args.url[0])


if __name__ == "__main__":
    main()
