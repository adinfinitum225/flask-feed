import psycopg2
import click

from flask import g
from flask.cli import with_appcontext

def check_db():
    """ Check connection to the PostgreSQL server """
    conn = None
    
    try:
        #connect to the server
        print('Connecting to the PostgreSQL server')
        #conn = psycopg2.connect(dbname="funneldb", user="zachwells", password="zwells225")
        conn = get_db()

        #create cursor
        cur = conn.cursor()
        
        #Do a thing
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        #Print version
        db_version = cur.fetchone()
        print(db_version)

        #Close the cursor
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            close_db()
            print('Database connection is closed')

def get_db():
    """ Return a PostgreSQL connection for the current request """
    conn = None

    if 'conn' not in g:
        try:
            g.conn = psycopg2.connect(dbname="funneldb", user="zachwells", password="zwells225")
        except (Exception, psycopg2.DatabaseError) as error:
            flash(error)
            pass

    return g.conn

def close_db():
    """ Close the PostgreSQL connection """
    conn = g.pop('conn', None)

    if conn is not None:
        conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(check_db_command)

@click.command('test-db')
@with_appcontext
def check_db_command():
    check_db()
