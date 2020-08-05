import os

from flask import Flask, jsonify, Response
from flask_cors import CORS
from flask_migrate import Migrate
from whitebearbake.database.models import *



migrate = Migrate()

class Config(object):    

    # Connect to the database
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    if FLASK_ENV ==  'development':
        SQLALCHEMY_DATABASE_URI = 'postgresql://capstone_usr:mypass@localhost:5432/capstone_dev'
        DEBUG = True
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)
        DEBUG = False

def create_app(cfg=None):
    """ Define the app object and instantiate context """
    # Instantiate app object
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
    # app = Flask(__name__,static_folder=static_dir, template_folder=template_dir, static_url_path='')
    app = Flask(__name__)
    app.config.from_object(Config())
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("SQLALCHEMY_DATABASE_URI cannot be found in config. "
        "please environment variable 'DATABASE_URI'")
    app.logger.debug("SQLALCHEMY_DATABASE_URI:{}".format(app.config['SQLALCHEMY_DATABASE_URI']))
    # Instantiate CORS
    CORS(app)
    # api routes

    from whitebearbake.api import bp as api
    app.register_blueprint(api, url_prefix='/api')

    # UI routes
    from whitebearbake.ui import bp as ui
    app.register_blueprint(ui, url_prefix='/')

    from whitebearbake.database import db
    from whitebearbake.api.schemas import ma
    # attach app to migrate object
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    app.app_context().push()
    
    return app