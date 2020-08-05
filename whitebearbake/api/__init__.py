from flask import abort, Blueprint, current_app, request, url_for
from flask_restful import Api
from werkzeug.exceptions import HTTPException


from whitebearbake.database import db
from whitebearbake.api.apierror import ApiError
from whitebearbake.api.resources.ingredientNameResouce import *
# Instantiate blueprint class
bp = Blueprint('api', __name__)
api = Api(bp)
api.add_resource(IngredientNameResouce,'/ingredientNames')

@bp.route('/', methods=['GET'])
def root():
    """ Blueprint root route """
    return {'message': 'Welcome to WhiteBearBake API', 'status_code': '200', 'status': 'success', 'data': None}

@bp.teardown_request
def teardown(exception=None):
    # print("before tear down sessiion:{0}".format(str(db.session)))
    if exception:

        current_app.logger.error("teardown with error, error message: {0}".format(exception))
        current_app.error("teardown_request - rolling back active database sessions.")
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

# Register errorhandler for specific HTTP codes
for code in (400, 401, 403, 404, 405, 409, 410, 412, 413, 418, 429, 500, 501, 502, 503, 504, 505):
    bp.errorhandler(code)(handle_abort)
