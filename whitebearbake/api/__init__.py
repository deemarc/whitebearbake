from flask import abort, Blueprint, current_app, request, url_for

# Instantiate blueprint class
bp = Blueprint('api', __name__)
@bp.route('/', methods=['GET'])
def root():
    print('hellll')
    """ Blueprint root route """
    return {'message': 'Welcome to WhiteBearBake API', 'status_code': '200', 'status': 'success', 'data': None}