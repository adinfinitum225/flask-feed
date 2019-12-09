from xml.etree.ElementTree import parse
from urllib.request import urlopen, urljoin
from urllib.parse import urlsplit

from . import atomparse
from . import rssparse

def filter_feed(url):
    with urlopen(url) as response:
        tree = parse(response)
    root = tree.getroot()
    if root.tag == 'rss':
        return rssparse.filter_feed(tree)
    else:
        return atomparse.filter_feed(tree)

def normalize_url(url):
    url = url.casefold()
    url = url.strip()
    url = url.split('www.')
    url = url[-1].split('//')
    url = urljoin('https://', ('//' + url[-1]))

    return url
