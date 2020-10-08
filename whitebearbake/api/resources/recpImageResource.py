# import flask package
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

# import inside the package
from whitebearbake.api import bp
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api.schemas import RecpImageSchema, RecpImageSchemaPOST
from whitebearbake.api.decorators import jSend

from whitebearbake.database import db
from whitebearbake.database.models import RecpImage





apiHandle = masqlapi(db.session, RecpImage ,RecpImageSchema, RecpImageSchemaPOST)

@bp.route('/recpimages', methods=['GET'])
@jSend
def get_recpImage_resource():
    """
    Get list of recpImages that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for recpImages 
        operationId: get_recpImage
        tags:
         - recpImage
        parameters:
          - name: id
            in: query
            required: false
            description: recpImages resource identifier
            schema:
              type: int
          - name: image_link
            in: query
            description: recpImages's image_link
            required: false
            schema:
              type: string
        responses:
            200:
                description: recpImagess to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecpImages"
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

@bp.route('/recpimages', methods=['POST'])
@jSend
def post_recpImage_resource():
    """
    Create new recpImage with given parameter inside request body
    ---
    post:
        description: Create new recpImage with given parameter inside request body
        operationId: post_recpImage
        tags:
         - recpImage
        responses:
            201:
                description: return recpImage item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecpImage"
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
                $ref: "#/components/schemas/RecpImageSchemaPOST"
              
    """
    return apiHandle.post("image_link")
        
@bp.route('/recpimages/<id>', methods=['GET'])
@jSend
def get_single_recpImage_resource(id):
    """
    Get specific RecpImage by the id
    ---
    get:
        description: Get specific RecpImage
        operationId: get_single_recpImage
        tags:
         - recpImage
        parameters:
          - name: id
            in: path
            description: RecpImage's id
            required: true
            schema:
              type: string
            
        responses:
            200:
                description: RecpImages to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecpImage"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/recpimages/<id>', methods=['PATCH'])
@jSend
def patch_single_recpImage_resource(id):
    """
    Modifies specific RecpImage by the id
    ---
    patch:
        description: Modifies specific RecpImage
        operationId: patch_single_recpImage
        tags:
         - recpImage
        parameters:
          - name: id
            in: path
            description: RecpImage's id
            required: true
            schema:
              type: string
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/RecpImageSchemaPOST"
        responses:
            200:
                description: RecpImages to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecpImage"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/recpimages/<id>', methods=['DELETE'])
@jSend
def delete_single_recpImage_resource(id):
    """
    delete specific recpImage by the id
    ---
    delete:
        description: Delete specific recpImage
        operationId: delete_single_recpImage
        tags:
         - recpImage
        parameters:
          - name: id
            in: path
            description: recpImage's id
            required: true
            schema:
              type: string
        responses:
            200:
                description: successfully deleted recpImages entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)