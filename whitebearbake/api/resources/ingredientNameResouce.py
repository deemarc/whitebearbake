from flask import request, abort, jsonify, current_app
from flask_restful import Resource

from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

from whitebearbake.api.schemas import IngredienNameSchema, IngredienNameSchemaPOST
from whitebearbake.database import db
from whitebearbake.database.models import IngredientName
from whitebearbake.api.apierror import ApiError
# from whitebearbake.api.resources.restive import Restive
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api import bp
from whitebearbake.api.decorators import jSend

# apiHandle = Restive(IngredientName,IngredienNameSchema)
apiHandle = masqlapi(db.session, IngredientName,IngredienNameSchema, IngredienNameSchemaPOST)

@bp.route('/ingredientNames', methods=['GET'])
@jSend
def get_ingredient_name_resource():
    """
    Get list of ingredientName that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for ingredient name
        operationId: get_ingredient_name
        tags:
         - ingredientName
        parameters:
          - name: id
            in: query
            required: false
            description: ingredientName resource identifier
            schema:
              type: int
          - name: name
            in: query
            description: ingredientName's Name
            required: false
            schema:
              type: string
        responses:
            200:
                description: ingredientNames to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientNames"
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

@bp.route('/ingredientNames', methods=['POST'])
def post_ingredient_name_resource():
    """
    Create new ingredientName with given parameter inside request body
    ---
    post:
        description: Create new ingredientName with given parameter inside request body
        operationId: post_ingredient_name
        tags:
         - ingredientName
        responses:
            201:
                description: return IngredientName item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientName"
            200:
                description: Item Already exist
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
        parameters:
          - name: body
            in: body
            description: Action payload
            required: true
            schema:
              $ref: "#/components/schemas/IngredienNameRequest"

    """
    return apiHandle.post("name")
        
@bp.route('/ingredientNames/<str:name>', methods=['GET'])
def get_single_ingredient_name_resource(name):
    """
    Get specific ingredientName by the name
    ---
    get:
        description: Get specific ingredientName
        operationId: get_single_ingredient_name
        tags:
         - ingredientName
        responses:
            200:
                description: ingredientNames to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientName"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(name=name) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/ingredientNames/<str:name>', methods=['PATCH'])
def patch_single_ingredient_name_resource(name):
    """
    Modifies specific ingredientName by the name
    ---
    patch:
        description: Modifies specific ingredientName
        operationId: patch_single_ingredient_name
        tags:
         - ingredientName
        responses:
            200:
                description: ingredientNames to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendIngredientName"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(name=name) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/ingredientNames/<str:name>', methods=['DELETE'])
def delete_single_ingredient_name_resource(name):
    """
    delete specific ingredientName by the name
    ---
    patch:
        description: Delete specific ingredientName
        operationId: delete_single_ingredient_name
        tags:
         - ingredientName
        responses:
            200:
                description: successfully deleted ingredientNames entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    obj = apiHandle.get(name=name) or abort(404)
    return apiHandle.delete(obj)

# # for query single item using ingredient name
# class IngredientNameSingle(Resource):
#     def get(self,name):
#         obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")

#         return apiHandle.dump(obj,many=False), 200 

#     def patch(self,name):
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({"status":"fail", "messagge":"recive empty body"}),400
#         patch_data = apiHandle.load(json_data,partial=True)
#         obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")
#         obj = apiHandle.patch(obj,patch_data)
#         return apiHandle.dump(obj,many=False), 200 

#     def delete(self,o):
#         obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")
#         return apiHandle.delete(obj), 200

