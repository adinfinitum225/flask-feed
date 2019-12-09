from urllib.request import urlopen

from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
        )

from funnel.filter.parsehelp import filter_feed, normalize_url
from funnel.db import get_db

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
    feeds = []
    for url in urls:
        url = normalize_url(url[0])
        feed = filter_feed(url)
        feeds.append(feed)
    return feeds
