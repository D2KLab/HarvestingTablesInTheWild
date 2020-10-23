#!/usr/bin/env python3

import argparse
import sys

import requests

def main():
    parser = argparse.ArgumentParser(prog='crawlinator.py',
                                     description='Fetches and extracts table from HTML pages')
    parser.add_argument('url', nargs='*', action='append')
    args = parser.parse_args()
    if len(args.url[0]) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)
    for url in args.url[0]:
        pipeline(url)

def pipeline(url: str):
    html = fetch(url)
    table = extract_table(html)
    print(table)

def fetch(url: str) -> str:
    # by default, requests will follow redirects
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError('Failed to fetch', url, ', status code:', resp.status_code)

    return resp.text

def extract_table(html: str) -> str:
    _ = html
    return 'TODO: extract table'

if __name__ == "__main__":
    main()
