import csv
import os
from functools import reduce
from typing import Iterable, Dict, List

from bs4 import BeautifulSoup

from core.parsing.exceptions import InvalidTableException


MIN_BODY_ROWS = 2

def clean_whitespace(text: str) -> str:
    text = text.replace('\t', ' ')  # replace tabs with withspace
    text = text.replace('\r', ' ')  # replace end-of-line with withspace
    text = text.replace('\n', ' ')  # replace newlines with withspace
    text = text.strip()  # remove leading / trailing whitespace
    return text


def parse_inner_text_from_html(html: str) -> str:
    bs = BeautifulSoup(html)
    return clean_whitespace(bs.text)

def get_term_set(html: str) -> List[str]:
    """
    Returns the 100 most common terms (words) on the web page,
    sorted in descending order
    """
    _ = html.css('body *::text').getall()
    # TODO

    return [""]

def validate_body_cell_layout(rows: Iterable[List]):  # pylint: disable=useless-return
    """
    Checks that the layout of the table body is regular, i.e.
    that there is no row with more columns than the most
    common number of columns
    Raises InvalidTableException when a requirements is not satisfied
    """
    if len(rows) < MIN_BODY_ROWS:
        raise InvalidTableException(f'Table only has {len(rows)} rows, min: {MIN_BODY_ROWS}')

    row_cols = {}
    for row in rows:
        row_cols[len(row)] = row_cols.get(len(row), 0) + 1

    most_common_cols = max(row_cols, key=row_cols.get)
    max_cols = max(row_cols)
    if max_cols > most_common_cols:
        raise InvalidTableException('Maximum number of columns exceed most common number of columns')

    return None


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
