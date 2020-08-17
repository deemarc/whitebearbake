from flask import abort, Blueprint, current_app, request, url_for, jsonify
# from flagger import Api
from werkzeug.exceptions import HTTPException
import socket
import os
import time

from whitebearbake.database import db
from whitebearbake.api.apierror import ApiError
# from whitebearbake.api.schemas import *
from flask_apispec.extension import FlaskApiSpec
# Instantiate blueprint class
bp = Blueprint('api', __name__)

# api.add_resource(IngredientNameSingle,'/ingredientNames/<name>')


def test_engine(engine):
    """ Tests SQLAlchemy engine and returns response time """
    if not engine:
        return {'status': 'ERROR', 'error': 'No engine defined'}
    try:
        start = time.time()
        connection = engine.connect()
        if not connection.closed:
            connection.close()
        elapsed = '{:.3f}'.format(time.time() - start)
        return {
            'engine': str(engine),
            'label': getattr(engine, 'label', '<unknown>'),
            'status': 'OK',
            'time': elapsed
        }
    except Exception as err:
        return {'status': 'ERROR', 'error': str(err)}


@bp.route('/', methods=['GET'])
def root():
    """ Blueprint root route """
    return {'message': 'Welcome to WhiteBearBake API', 'status_code': '200', 'status': 'success', 'data': None}

@bp.route('/monitor', methods=['GET'])
def monitor():
    """ Global monitoring route """
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    poolid = pool_chk_in = pool_chk_out = None
    if db.session.bind :
        poolid = id(db.session.bind.pool)
        pool_chk_in =  db.session.bind.pool.checkedin()
        pool_chk_out =  db.session.bind.pool.checkedout()


    payload = {
        'app': current_app.name,
        'node': socket.gethostname().lower(),
        'status': 'OK',
        'proxy' : os.environ.get('proxy'),
        # 'cache' : CacheConfig.CACHE_TYPE ,
        #'debug' : config.get('DEBUG')
        'client_ip' : user_ip,
        'connection_pool' : {'id':poolid,
                           'checked_in' : pool_chk_in,
                           'checked_out' : pool_chk_out
        }
    }

    current_app.testing = True

    


    with current_app.app_context():

        payload['status'] = 'OK'
        payload['dependencies'] = {}

    #     # Blueprints for V3
    #     payload['v3']['dependencies']['admin_v3'] = test_blueprint(client, '/admin/v3')
    #     payload['v3']['dependencies']['api_v3'] = test_blueprint(client, '/api/v3')
    #     payload['v3']['dependencies']['ui_v3'] = test_blueprint(client, '/v3')

        # Engines for V1
        payload['dependencies']['engine'] = test_engine(db.session.bind)

        for k, v in payload['dependencies'].items():
            if v.get('status') != 'OK':
                payload['status'] = 'ERROR'
                payload['status'] = 'ERROR'
                if 'engine' in k:
                    db.configure()

        if payload['status'] == 'ERROR':
            return payload, 500

        return payload, 200
@bp.teardown_request
def teardown(exception=None):
    # print("before tear down sessiion:{0}".format(str(db.session)))
    if exception:

        current_app.logger.error("teardown with error, error message: {0}".format(exception))
        current_app.logger.error("teardown_request - rolling back active database sessions.")
        db.session.rollback()
        
    db.session.close()
    db.session.remove()

@bp.errorhandler(HTTPException)
def handle_abort(err):
    """ Register abort handler on blueprint. """
    if not isinstance(err.description, (list, tuple)):
        err.description = [err.description]
    return {'message': err.name, 'errors': err.description}, err.code

@bp.errorhandler(Exception)
def exception_handler(error):
    if db.session:
        db.session.rollback()
    err = ApiError(500,500,str(type(error))+':'+str(error))
    current_app.logger.exception(err)
    # logger.exception(error)
    return jsonify(err.error), err.status_code

# @bp.errorhandler(Exception)
# def handle_exception(err):
#     if db.session:
#         db.session.rollback()
#     """ Register unhandled exception handler on blueprint """
#     current_app.logger.error('Unhandled Exception : ' + str(err), exc_info=True, extra={'mail': True})
#     return {'message': 'Internal Server Exception', 'errors': ['An unhandled exception has occurred', 'Exception: ' + str(err)]}, 500


@bp.route('/abort/<code>', methods=['GET'])
@bp.route('/abort/<code>/<message>', methods=['GET'])
def route_abort(code, message=None):
    """ Custom abort route """
    if message:
        abort(int(code), message)
    abort(int(code))

@bp.route('/except/<err>', methods=['GET'])
@bp.route('/except/<err>/<message>', methods=['GET'])
def route_except(err, message=None):
    """ Custom exception route """
    exception = eval(err)
    if message:
        raise exception(str(message))
    raise exception()

@bp.route("/<path:invalid_path>", methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
def route404(*args, **kwargs):
    """ Catch all route within blueprint to force use of 404 errorhandler. """
    abort(404)

from . resources import swagger, ingredientNameResouce
# Register errorhandler for specific HTTP codes
for code in (400, 401, 403, 404, 405, 409, 410, 412, 413, 418, 429, 500, 501, 502, 503, 504, 505):
    bp.errorhandler(code)(handle_abort)


