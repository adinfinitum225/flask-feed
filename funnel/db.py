import psycopg2
import click

from flask import current_app, g
from flask.cli import with_appcontext

def check_db():
    """ Connect to the PostgreSQL server """
    conn = None
    
    try:
        #connect to the server
        print('Connecting to the PostgreSQL server')
        conn = psycopg2.connect(dbname="funneldb", user="zachwells", password="zwells225")

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
            conn.close()
            print('Database connection closed')

def init_app(app):
    app.cli.add_command(check_db_command)

@click.command('test-db')
@with_appcontext
def check_db_command():
    check_db()
