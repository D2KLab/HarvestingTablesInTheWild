import os

from scrapy.http.response.text import TextResponse

from core.spiders.web import TableParserSpider
from core.spiders.fixtures.w3_schools import w3_schools
from core.spiders.fixtures.wiki_nhl import wiki_nhl


def run_test(url, html, expected_output):
    resp = TextResponse(url, body=html)
    os.environ['URL_STRING'] = url
    got = list(TableParserSpider().parse(resp))
    del os.environ['URL_STRING']

    # patch timestamp field
    for t in got:
        t.timestamp = 'FAKE'

    # test each item individually (improves readability of the diff)
    assert len(got) == len(expected_output)
    for i, _ in enumerate(got):
        assert got[i] == expected_output[i]


def test_parse_w3_html_tables():
    run_test(*w3_schools())


def test_parse_wikipedia_nhl():
    run_test(*wiki_nhl())
