import os

import pytest

from scrapy.http.response.text import TextResponse

from core.spiders.web import TableParserSpider
from core.spiders.fixtures.w3_schools import w3_schools
from core.spiders.fixtures.wiki_nhl import wiki_nhl


def test_parse_w3_html_tables(w3_schools):
    url, html, expected_output = w3_schools

    resp = TextResponse(url, body=html)
    os.environ['URL_STRING'] = url
    got = list(TableParserSpider().parse(resp))
    del os.environ['URL_STRING']

    # patch timestamp field
    for t in got:
        t.timestamp = 'FAKE'

    assert got == expected_output

def test_parse_wikipedia_nhl(wiki_nhl):
    url, html, expected_output = wiki_nhl

    resp = TextResponse(url, body=html)
    os.environ['URL_STRING'] = url
    got = list(TableParserSpider().parse(resp))
    del os.environ['URL_STRING']

    # patch timestamp field
    for t in got:
        t.timestamp = 'FAKE'

    assert got == expected_output
