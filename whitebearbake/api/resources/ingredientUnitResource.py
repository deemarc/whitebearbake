# import flask package
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

# import inside the package
from whitebearbake.api import bp
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api.schemas import IngredientUnitSchema, IngredientUnitSchemaPOST
from whitebearbake.api.decorators import jSend

from whitebearbake.database import db
from whitebearbake.database.models import IngredientUnit





apiHandle = masqlapi(db.session, IngredientUnit,IngredientUnitSchema, IngredientUnitSchemaPOST)

@bp.route('/ingredientUnits', methods=['GET'])
@jSend
def get_ingredient_unit_resource():
    """
    Get list of ingredientUnit that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for ingredient name
        operationId: get_ingredient_unit
        tags:
         - ingredientUnit
        parameters:
          - name: id
            in: query
            required: false
            description: ingredientUnit resource identifier
            schema:
              type: int
          - name: name
            in: query
            description: ingredientUnit's Name
            required: false
            schema:
              type: string
        responses:
            200:
                description: ingredientUnits to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientUnits"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    filters = request.args
    objs = apiHandle.get_many(**filters)
    return apiHandle.getMethod(objs, many=True)

    # return jsonify(apiHandle.dump(objs,many=True)), 200

@bp.route('/ingredientUnits', methods=['POST'])
@jSend
def post_ingredient_unit_resource():
    """
    Create new ingredientUnit with given parameter inside request body
    ---
    post:
        description: Create new ingredientUnit with given parameter inside request body
        operationId: post_ingredient_unit
        tags:
         - ingredientUnit
        responses:
            201:
                description: return ingredientUnit item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientUnit"
            200:
                description: Item Already exist
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/IngredientUnitSchemaPOST"
              

    """
    return apiHandle.post("name")
        
@bp.route('/ingredientUnits/<id>', methods=['GET'])
@jSend
def get_single_ingredient_unit_resource(id):
    """
    Get specific ingredientUnit by the name
    ---
    get:
        description: Get specific ingredientUnit
        operationId: get_single_ingredient_unit
        tags:
         - ingredientUnit
        parameters:
          - name: name
            in: path
            description: ingredientUnit's Name
            required: true
            schema:
              type: string
            
        responses:
            200:
                description: ingredientUnits to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientUnit"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/ingredientUnits/<id>', methods=['PATCH'])
@jSend
def patch_single_ingredient_unit_resource(id):
    """
    Modifies specific ingredientUnit by the name
    ---
    patch:
        description: Modifies specific ingredientUnit
        operationId: patch_single_ingredient_unit
        tags:
         - ingredientUnit
        parameters:
          - name: name
            in: path
            description: ingredientUnit's Name
            required: true
            schema:
              type: string
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/IngredientUnitSchemaPOST"
        responses:
            200:
                description: ingredientUnits to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientUnit"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/ingredientUnits/<id>', methods=['DELETE'])
@jSend
def delete_single_ingredient_unit_resource(id):
    """
    delete specific ingredientUnit by the name
    ---
    delete:
        description: Delete specific ingredientUnit
        operationId: delete_single_ingredient_unit
        tags:
         - ingredientUnit
        parameters:
          - name: name
            in: path
            description: ingredientUnit's Name
            required: true
            schema:
              type: string
        responses:
            200:
                description: successfully deleted ingredientUnits entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)


