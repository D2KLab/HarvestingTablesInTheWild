from urllib.parse import urlparse
from typing import Iterable
import re

class CrawlingStrategy:
    """
    Class implementing the two tier approach for selecting which webpages to crawl.
    """

    @classmethod
    def __init__(cls, follow_links=False):
        cls.follow_links = follow_links

    # Note: r'^(.*\.|)' matches the domain itself including any subdomains
    tier_one_regexes = [re.compile(i) for i in [
        r'^en\.wikipedia\.org',
        r'^(.*\.|)android\.com',
        r'^(.*\.|)apache\.org',
        r'^(.*\.|)bbc\.co\.uk',
        r'^(.*\.|)blogspot\.com',
        r'^(.*\.|)creativecommons\.org',
        r'^(.*\.|)doi\.org',
        r'^(.*\.|)europe\.eu',
        r'^(.*\.|)gamepedia\.com',
        r'^(.*\.|)github\.com',
        r'^(.*\.|)github\.io',
        r'^(.*\.|)iana\.org',
        r'^(.*\.|)imdb\.com',
        r'^(.*\.|)medium\.com',
        r'^(.*\.|)merriam-webster\.com',
        r'^(.*\.|)microsoft\.com',
        r'^(.*\.|)mozilla\.org',
        r'^(.*\.|)nasa\.gov',
        r'^(.*\.|)nih\.gov',
        r'^(.*\.|)noaa\.gov',
        r'^(.*\.|)schema\.org',
        r'^(.*\.|)statista\.com',
        r'^(.*\.|)w\.org',
        r'^(.*\.|)wikibooks\.org',
        r'^(.*\.|)wikimedia\.org',
        r'^(.*\.|)wikiquote\.org',
        r'^(.*\.|)wordpress\.com',
        r'^(.*\.|)wordpress\.org',
    ]]

    blacklist_regexes = [re.compile(i) for i in [
        r'^(?!.*(en)).*\.wikipedia\.org', # blacklist everything except en.wikipedia.org
        r'^(?!.*(en)).*\.wiki.*\.org', # blacklist everything except english wikis
        r'^.*\.m\..*', # blacklist mobile pages
        r'example\.org', # for testing purposes, no tables here anyway
    ]]

    @classmethod
    def __is_blacklisted(cls, domain: str) -> bool:
        for regex in cls.blacklist_regexes:
            if regex.fullmatch(domain) is not None:
                return True

        return False

    @classmethod
    def __is_tier_one(cls, domain: str) -> bool:
        for regex in cls.tier_one_regexes:
            if regex.fullmatch(domain) is not None:
                return True

        return False

    @classmethod
    def get_links_to_follow(cls, url, html) -> Iterable[str]:
        "Extracts and filters all links that should be crawled according to strategy"

        if not cls.follow_links:
            # only do deep crawls when follow_links is enabled
            yield from ()
            return

        domain = cls.__get_domain_from_url(url)
        if not cls.__is_tier_one(domain):
            # this is a tier 2 website, stop crawling here
            yield from () # return empty generator
            return

        # extract all hyperrefs
        all_links = html.css('a::attr(href)').getall()

        for link in all_links:

            # skip internal page references, mailto, javascript and tel links
            if link.startswith('#') or \
               link.startswith('mailto:') or \
               link.startswith('javascript:') or \
               link.startswith('tel:'):
                continue

            # relative urls are always allowed (same domain)
            if link.startswith('/') and not link.startswith('//'):
                yield link
                continue

            # only external references left
            # check if their domain is blacklisted
            link_domain = cls.__get_domain_from_url(link)
            if cls.__is_blacklisted(link_domain):
                continue

            yield link

    @classmethod
    def __get_domain_from_url(cls, url: str) -> str:
        o = urlparse(url)
        return o.netloc.split(':')[0]
