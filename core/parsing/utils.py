import csv
import os
from functools import reduce
from typing import Iterable, Dict
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from core.parsing.exceptions import InvalidTableException
from core.parsing.parsers import TableParser, WikitableParser, WellFormattedTableParser


def clean_whitespace(text: str) -> str:
    text = text.replace('\t', ' ')  # replace tabs with withspace
    text = text.strip()  # remove leading / trailing whitespace
    return text


def parse_inner_text_from_html(html: str) -> str:
    bs = BeautifulSoup(html)
    return clean_whitespace(bs.text)


def get_title_from_text(response) -> str:
    return response.css('title::text').getall()[0]


def compose_normalized_table(headers: Iterable, rows: Iterable) -> Dict:
    '''
    Parameters:
    headers: header row of the table
    rows: a 2-dimensional list (matrix) that contains
    the data rows for the given table. Eg. cell = rows[row_index][column_index]

    Returns:
    Table in object notation.
    For example:
    >>> compose_normalized_table(["header1","header2"],[[1,2],[3,4]])
    {'header1': [1, 3], 'header2': [2, 4]}

    '''
    try:
        normalized_table = reduce(lambda composition, next_header: {
            **composition, next_header: []}, headers, {})
        for row in rows:
            for index, cell in enumerate(row):
                normalized_table[headers[index]].append(cell)
        return normalized_table
    except IndexError as e:
        raise InvalidTableException() from e


def get_url_list_from_environment():
    url_string = os.environ.get('URL_STRING')
    url_file = os.environ.get('URL_FILE')

    if url_string:
        urls = url_string.split(',')
    elif url_file:
        with open(url_file, 'r') as fd:
            urls = []
            for row in csv.reader(fd):
                urls.append(row[0])
    else:
        raise Exception(
            'Need to either specify URL_STRING or URL_FILE')
    if len(urls) == 0:
        raise Exception('No URLs found from provided resource')
    return urls


def get_parser_from_url(url: str) -> TableParser:
    o = urlparse(url)
    if "wikipedia.org" in o.netloc:
        return WikitableParser()
    return WellFormattedTableParser()
