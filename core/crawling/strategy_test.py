import pytest
import os

from scrapy.selector import Selector

from core.crawling.strategy import CrawlingStrategy

def test_crawling_strategy():
    cs = CrawlingStrategy(follow_links=True)
    html = Selector(text='''
    <html><body>
    <a href="https://en.wikipedia.org/index.php"></a>
    <a href="https://abc.wikipedia.org/index.php"></a>
    <a href="https://example.com/index.html"></a>
    <a href="/relative/link"></a>
    <a href="http://example.org"></a>
    <a href="#internal-reference"></a>
    <a href="mailto:max@example.com"></a>
    <a href="javascript:alert();"></a>
    <a href="tel:1234"></a>
    </body></html>
    ''')

    # here we are on a tier one domain, so all links should be followed, except the blacklisted ones
    links = list(cs.get_links_to_follow("//en.wikipedia.org/index.php", html))
    assert 'https://en.wikipedia.org/index.php' in links
    assert 'https://example.com/index.html' in links
    assert '/relative/link' in links
    assert not 'https://abc.wikipedia.org/index.php' in links
    assert not 'http://example.org' in links
    assert not '#internal-reference' in links
    assert not 'mailto:max@example.com' in links
    assert not 'javascript:alert();' in links
    assert not 'tel:1234' in links
    assert len(links) == 3

    # here we are on tier two domain, so we don't follow any links
    links = list(cs.get_links_to_follow("https://example.com/example.html", html))
    assert len(links) == 0

def test_crawling_follow():
    html = Selector(text='<a href="https://en.wikipedia.org/index.php"></a>')
    links = list(
        CrawlingStrategy(follow_links=True).
        get_links_to_follow("//en.wikipedia.org/", html)
    )
    assert len(links) == 1

def test_crawling_no_follow():
    html = Selector(text='<a href="https://en.wikipedia.org/index.php"></a>')
    links = list(
        CrawlingStrategy(follow_links=False).
        get_links_to_follow("//en.wikipedia.org/", html)
    )
    assert len(links) == 0
