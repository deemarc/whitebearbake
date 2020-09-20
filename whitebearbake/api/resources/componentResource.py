# import flask package
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

# import inside the package
from whitebearbake.api import bp
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api.schemas import ComponentSchema, ComponentSchemaPost
from whitebearbake.api.decorators import jSend

from whitebearbake.database import db
from whitebearbake.database.models import Component





apiHandle = masqlapi(db.session, Component ,ComponentSchema, ComponentSchemaPost)

@bp.route('/components', methods=['GET'])
@jSend
def get_component_resource():
    """
    Get list of ingredient that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for ingredient name
        operationId: get_component
        tags:
         - ingredient
        parameters:
          - name: id
            in: query
            required: false
            description: ingredient resource identifier
            schema:
              type: int
          - name: name
            in: query
            description: ingredient's Name
            required: false
            schema:
              type: string
        responses:
            200:
                description: ingredients to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredients"
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

@bp.route('/components', methods=['POST'])
@jSend
def post_component_resource():
    """
    Create new ingredient with given parameter inside request body
    ---
    post:
        description: Create new ingredient with given parameter inside request body
        operationId: post_component
        tags:
         - ingredient
        responses:
            201:
                description: return ingredient item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredient"
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
                $ref: "#/components/schemas/ComponentSchemaPOST"
              

    """
    return apiHandle.post("name")
        
@bp.route('/ingredients/<id>', methods=['GET'])
@jSend
def get_single_component_resource(name):
    """
    Get specific ingredient by the name
    ---
    get:
        description: Get specific ingredient
        operationId: get_single_component
        tags:
         - ingredient
        parameters:
          - name: name
            in: path
            description: ingredient's Name
            required: true
            schema:
              type: string
            
        responses:
            200:
                description: ingredients to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredient"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(name=name) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/components/<id>', methods=['PATCH'])
@jSend
def patch_single_component_resource(id):
    """
    Modifies specific ingredient by the name
    ---
    patch:
        description: Modifies specific ingredient
        operationId: patch_single_component
        tags:
         - ingredient
        parameters:
          - name: name
            in: path
            description: ingredient's Name
            required: true
            schema:
              type: string
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/ComponentSchemaPOST"
        responses:
            200:
                description: ingredients to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredient"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/components/<id>', methods=['DELETE'])
@jSend
def delete_single_component_resource(id):
    """
    delete specific ingredient by the name
    ---
    delete:
        description: Delete specific ingredient
        operationId: delete_single_component
        tags:
         - ingredient
        parameters:
          - name: name
            in: path
            description: ingredient's Name
            required: true
            schema:
              type: string
        responses:
            200:
                description: successfully deleted ingredients entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)

