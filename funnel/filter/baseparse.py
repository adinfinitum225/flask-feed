from dataclasses import dataclass

@dataclass
class BaseFeed:
    title: str
    entries: list
    link: dict

@dataclass
class BaseEntry:
    title: str
    author: str
    updated: 'datetime'
    id: str

def filter_feed(tree):
    pass

def filter_entry(tree):
    pass


