# import flask package
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

# import inside the package
from whitebearbake.api import bp
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api.schemas import BakerSchema, BakerSchemaPOST
from whitebearbake.api.decorators import jSend

from whitebearbake.database import db
from whitebearbake.database.models import Baker





apiHandle = masqlapi(db.session, Baker ,BakerSchema, BakerSchemaPOST)

@bp.route('/bakers', methods=['GET'])
@jSend
def get_baker_resource():
    """
    Get list of baker that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for baker 
        operationId: get_baker
        tags:
         - baker
        parameters:
          - name: id
            in: query
            required: false
            description: baker resource identifier
            schema:
              type: int
          - name: name
            in: query
            description: baker's Name
            required: false
            schema:
              type: string
        responses:
            200:
                description: bakers to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendBakers"
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

@bp.route('/bakers', methods=['POST'])
@jSend
def post_baker_resource():
    """
    Create new baker with given parameter inside request body
    ---
    post:
        description: Create new baker with given parameter inside request body
        operationId: post_baker
        tags:
         - baker
        responses:
            201:
                description: return baker item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendBaker"
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
                $ref: "#/components/schemas/BakerSchemaPOST"
              
    """
    return apiHandle.post("name")
        
@bp.route('/bakers/<id>', methods=['GET'])
@jSend
def get_single_baker_resource(id):
    """
    Get specific baker by the id
    ---
    get:
        description: Get specific baker
        operationId: get_single_baker
        tags:
         - baker
        parameters:
          - name: id
            in: path
            description: baker's id
            required: true
            schema:
              type: int
            
        responses:
            200:
                description: bakers to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendBaker"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/bakers/<id>', methods=['PATCH'])
@jSend
def patch_single_baker_resource(id):
    """
    Modifies specific baker by the id
    ---
    patch:
        description: Modifies specific baker
        operationId: patch_single_baker
        tags:
         - baker
        parameters:
          - name: id
            in: path
            description: baker's id
            required: true
            schema:
              type: int
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/BakerSchemaPOST"
        responses:
            200:
                description: bakers to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendBaker"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/bakers/<id>', methods=['DELETE'])
@jSend
def delete_single_baker_resource(id):
    """
    delete specific baker by the id
    ---
    delete:
        description: Delete specific baker
        operationId: delete_single_baker
        tags:
         - baker
        parameters:
          - name: id
            in: path
            description: baker's id
            required: true
            schema:
              type: string
        responses:
            200:
                description: successfully deleted bakers entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)