from dataclasses import dataclass
from . import baseparse
from funnel.filter.parsehelp import ParseHelp

@dataclass
class RssFeed(baseparse.BaseFeed, ParseHelp):
    description: str
    
    @classmethod
    def filter_feed(cls, tree):
        root = tree.getroot()

        title = root.find('.//title')
        if title is not None:
            title = title.text
        link = root.find('.//link')
        if link is not None:
            link = {'href': link.text}
        description = root.find('.//description')
        if description is not None:
            description = description.text
        entries = root.findall('.//item')
        entries = [RssItem.filter_item(item) for item in entries]

        return RssFeed(title, entries, link, description)

@dataclass
class RssItem(baseparse.BaseEntry, ParseHelp):
    link: str
    description: str

    @classmethod
    def filter_item(cls, item):
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
        updated = item.find('pubDate')
        if updated is not None:
            updated = super().to_pydate(updated.text)
        id = item.find('guid')
        if id is not None:
            id = id.text

        return RssItem(title, author, updated, id, link, description)
