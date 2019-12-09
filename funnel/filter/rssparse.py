from urllib.request import urlopen
from xml.etree.ElementTree import parse
from dataclasses import dataclass

@dataclass
class RssFeed:
    title: str
    link: str
    description: str
    entries: list

@dataclass
class RssItem:
    title: str
    link: str
    description: str
    author: str
    pubdate: str
    guid: str

def filter_feed(tree):
    root = tree.getroot()

    title = root.find('.//title')
    if title is not None:
        title = title.text
    link = root.find('.//link')
    if link is not None:
        link = link.text
    description = root.find('.//description')
    if description is not None:
        description = description.text
    entries = root.findall('.//item')
    entries = [filter_item(item) for item in entries]

    return RssFeed(title, link, description, entries)

def filter_item(item):
    title = item.find('title')
    if title is not None:
        title = title.text
    link = item.find('link')
    if link is not None:
        link = link.text
    description = item.find('description')
    if description is not None:
        description = description.text
    author = item.find('author')
    if author is not None:
        author = author.text
    pubdate = item.find('pubDate')
    if pubdate is not None:
        pubdate = pubdate.text
    guid = item.find('guid')
    if guid is not None:
        guid = guid.text

    return RssItem(title, link, description, author, pubdate, guid)
