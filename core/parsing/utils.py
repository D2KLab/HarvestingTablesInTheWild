import csv
import os
from functools import reduce
from typing import Iterable, Dict, List
import itertools

from bs4 import BeautifulSoup
from scrapy.http.response.html import HtmlResponse

from core.parsing.exceptions import InvalidTableException


MIN_BODY_ROWS = 2

def clean_whitespace(text: str) -> str:
    # remove tabs, newlines and other whitespace (also leading/trailing)
    text = ' '.join(text.split())
    return text

def parse_inner_text_from_html(html: str) -> str:
    if not html:
        return ""

    bs = BeautifulSoup(html)
    return clean_whitespace(bs.text)

def get_text_after(element) -> str:
    html = element.xpath('./following-sibling::*[1]').get()
    return parse_inner_text_from_html(html)

def get_text_before(element) -> str:
    html = element.xpath('./preceding-sibling::*[1]').get()
    return parse_inner_text_from_html(html)

def is_in_form(element) -> bool:
    """
    Checks if the given selector is embedded in a <form> element
    """

    if not element:
        return False

    parent = element.xpath('..')

    # this condition indicates the end of the recursion
    if not parent:
        return False

    if parent.get().startswith('<form'):
        return True

    return is_in_form(parent)

def get_term_set(html) -> List[str]:
    """
    Returns the 100 most common terms (words) on the web page,
    sorted in descending order
    """
    if isinstance(html, str):
        fields = html.split() # split into fields
    elif isinstance(html, HtmlResponse):
        fields = html.css('body *::text').getall()
    else:
        raise TypeError('Type must by scrapy.HtmlResponse or str, got:  ' + type(html))

    # convert and reduce all whitespace characters
    cleaned_fields = map(clean_whitespace, fields)
    # split at word boundaries and flatten list
    split_fields =  list(itertools.chain(*[f.split() for f in cleaned_fields]))
    # cast all non-empty and non-whitespace fields to lowercase
    non_empty_fields = [f.lower() for f in split_fields if f and not f.isspace()]
    # accumulate to calculate frequencies
    term_freq = {}
    for f in non_empty_fields:
        term_freq[f] = term_freq.get(f, 0) + 1

    sorted_terms = [term for term, freq in sorted(term_freq.items(), key=lambda item: item[1], reverse=True)]

    # return at most 100 items
    return sorted_terms[0:100]

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
    return response.css('title::text').getall()[0] or ""

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
