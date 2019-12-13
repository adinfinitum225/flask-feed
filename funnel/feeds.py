from urllib.request import urlopen, urljoin
from urllib.parse import urlsplit
from xml.etree.ElementTree import parse

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
        )

from funnel.db import get_db
import funnel.filter.atomparse as aparse
import funnel.filter.rssparse as rparse

bp = Blueprint('feeds', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    if g.user is not None:
        cur.execute(
                'SELECT url FROM feeds WHERE username = %s',
                (g.user[0],)
                )
        urls = cur.fetchall()
        feeds = digest_feeds(urls)
    else:
        feeds = []
    
    return render_template('feeds/index.html', feeds=feeds)

@bp.route('/subscribe', methods=('POST',))
def subscribe():
    url = request.form['url']
    db = get_db()
    cur = db.cursor()

    xml_response = urlopen(url)

    cur.execute(
            'INSERT INTO feeds (username, url) VALUES (%s, %s)',
            (g.user, url)
            )

    db.commit()
    return redirect(url_for('feeds.index'))

def digest_feeds(urls):
    def filter_feed(url):
        with urlopen(url) as response:
            tree = parse(response)
        root = tree.getroot()
        if root.tag == 'rss':
            return rparse.RssFeed.filter_feed(tree)
        else:
            return aparse.AtomFeed.filter_feed(tree)

    feeds = []
    for url in urls:
        url = normalize_url(url[0])
        feed = filter_feed(url)
        feeds.append(feed)
    return feeds

    
def normalize_url(url):
    url = url.casefold()
    url = url.strip()
    url = url.split('www.')
    url = url[-1].split('//')
    url = urljoin('https://', ('//' + url[-1]))

    return url
