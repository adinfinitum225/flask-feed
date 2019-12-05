from urllib.request import urlopen
from xml.etree.ElementTree import parse
from dataclasses import dataclass


ns = {'atom': 'http://www.w3.org/2005/Atom'}

@dataclass
class AtomFeed:
    author: str
    title: str
    id: str
    updated: str
    link: dict
    entries: list

@dataclass
class AtomEntry:
    id: str
    title: str
    updated: str
    author: str
    content: str
    link: dict
    summary: str

def filter_feed(request):
    feed = parse(request)
    root = feed.getroot()

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
        updated = updated.text
    entries = root.findall('atom:entry', ns)
    entries = [filter_entry(entry) for entry in entries]

    return AtomFeed(author, title, id, updated, link, entries)

def filter_entry(entry):
    id = entry.find('atom:id', ns)
    if id is not None:
        id = id.text
    title = entry.find('atom:title', ns)
    if title is not None:
        title = title.text
    updated = entry.find('atom:updated', ns)
    if updated is not None:
        updated = updated.text
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

    return AtomEntry(id, title, updated, author, content, link, summary)
