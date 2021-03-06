import re
from urllib.request import urlopen, urljoin, Request
from urllib.parse import urlsplit
from xml.etree.ElementTree import parse

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for, request
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
                'SELECT url, id FROM feeds WHERE username = %s',
                (g.user[0],)
                )
        urls = cur.fetchall()
        feeds = digest_feeds(urls)
    else:
        feeds = []
    
    return render_template('feeds/index.html', feeds=feeds)

@bp.route('/subscribe', methods=('POST',))
def subscribe():
    #add error handling for http exceptions
    #add to make sure feed isn't duplicate
    url = request.form['url']
    db = get_db()
    cur = db.cursor()

    #Co-opt users User-Agent
    headers = {'User-Agent': request.headers.get('User-Agent')}
    req = Request(url=url, headers=headers)
    xml_response = urlopen(req)

    cur.execute(
            'INSERT INTO feeds (username, url) VALUES (%s, %s)',
            (g.user, url)
            )

    db.commit()
    return redirect(url_for('feeds.index'))

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    cur = db.cursor()

    cur.execute(
            'DELETE FROM feeds WHERE id = %s', (id,)
            )
    db.commit()
    return redirect(url_for('feeds.index'))

def digest_feeds(urls):
    def filter_feed(url):
        headers = {'User-Agent': request.headers.get('User-Agent')}
        req = Request(url=url, headers=headers)
        with urlopen(req) as response:
            tree = parse(response)
        root = tree.getroot()
        if root.tag == 'rss':
            return rparse.RssFeed.filter_feed(tree)
        else:
            return aparse.AtomFeed.filter_feed(tree)

    feeds = []
    
    for url in urls:
        url_name = normalize_url(url[0])
        feed = (filter_feed(url_name), url[1])
        feeds.append(feed)
    return feeds

    
#Make a separate norm for comparing urls vs subscribing?
def normalize_url(url):
    resource = re.search(r'/[^/]+$', url)
    end = resource.group()
    address = url[0:resource.start()]
    address = address.casefold()
    url = address + end
    url = url.strip()
    url = url.split('www.')
    url = url[-1].split('//')
    url = urljoin('https://', ('//' + url[-1]))

    return url
