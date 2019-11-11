import os

from flask import Flask

def create_app(test_config=None):
    #make my app and configure it and shit
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = 'dev',
            DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
            )
    if test_config is None:
        #load the instance config when no test config is passed to it
        app.config.from_pyfile('config.py', silent = True)
    else:
        #load the test config that is passed
        app.config.from_mapping(test_config)

    #make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a page that says Hola
    @app.route('/hello')
    def hello():
        return('Hola, World!')

    from . import db
    db.init_app(app)

    return app
