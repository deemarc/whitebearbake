from flask import abort, Blueprint, current_app, request, url_for
from flask_restful import Api

from whitebearbake.api.resources.ingredientNameResouce import *
# Instantiate blueprint class
bp = Blueprint('api', __name__)
api = Api(bp)
api.add_resource(IngredientNameResouce,'/ingredientNames')
@bp.route('/', methods=['GET'])
def root():
    print('hellll')
    """ Blueprint root route """
    return {'message': 'Welcome to WhiteBearBake API', 'status_code': '200', 'status': 'success', 'data': None}