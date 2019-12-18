from dataclasses import dataclass
from . import baseparse
from funnel.filter.parsehelp import ParseHelp

ns = {'atom': 'http://www.w3.org/2005/Atom'}

@dataclass
class AtomFeed(baseparse.BaseFeed, ParseHelp):
    author: str
    id: str
    updated: 'datetime'

    @classmethod
    def filter_feed(cls, tree):
        root = tree.getroot()

        author = root.find('atom:author', ns)
        if author is not None:
            author = author.text
        link = root.find('atom:link', ns)
        if link is not None:
            link = link.attrib
        id = root.find('atom:id', ns)
        if id is not None:
            id = id.text
        title = root.find('atom:title', ns)
        if title is not None:
            title = title.text
        updated = root.find('atom:updated', ns)
        if updated is not None:
            updated = super().to_pydate(updated.text)
        entries = root.findall('atom:entry', ns)
        entries = [AtomEntry.filter_entry(entry) for entry in entries]

        return AtomFeed(title, entries, author, id, updated, link)



@dataclass
class AtomEntry(baseparse.BaseEntry, ParseHelp):
    content: str
    link: dict
    summary: str

    @classmethod
    def filter_entry(cls, entry):
        id = entry.find('atom:id', ns)
        if id is not None:
            id = id.text
        title = entry.find('atom:title', ns)
        if title is not None:
            title = title.text
        updated = entry.find('atom:updated', ns)
        if updated is not None:
            updated = super().to_pydate(updated.text)
        author = entry.find('atom:author', ns)
        if author is not None:
            author = author.text
        content = entry.find('atom:content', ns)
        if content is not None:
            content = content.text
        link = entry.find('atom:link', ns)
        if link is not None:
            link = link.attrib
        summary = entry.find('atom:summary', ns)
        if summary is not None:
            summary = summary.text

        return AtomEntry(title, author, updated, id, content, link, summary)
