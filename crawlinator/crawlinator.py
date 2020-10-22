#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(prog=__name__, description='TODO')
    parser.add_argument('url', nargs='*', action='append')
    args = parser.parse_args()
    for u in args.url[0]:
        pipeline(u)

def pipeline(url: str):
    print(fetch(url))

def fetch(url: str) -> str:
    return 'TODO: fetch ' + url

if __name__ == "__main__":
    main()
