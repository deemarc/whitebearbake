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
            schema:
              type: int
          - name: name
            in: query
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
        parameters:
          - name: body
            in: body
            required: true
            schema:
              $ref: "#/components/schemas/IngredienNameRequest"
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
            401:
                description: Unauthorized
            403:
                description: Forbidden
            409:
                description: Conflict
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error

    """
    return apiHandle.post("name")
    # json_data = request.get_json()
    # if not json_data:
    #     return jsonify({"status":"fail", "messagge":"recive empty body"}),400

    # load_data = apiHandle.load(json_data)
    # current_app.logger.info(f"data to post:{load_data}")
    # isExist = apiHandle.get(name=load_data["name"])
    # if isExist:
    #     return abort(400,"IngredientName:{} already exist".format(load_data["name"]))
    # apiHandle.post(load_data)   
    # obj = IngredientName(**load_data)
    # ingrd_name_data = apiHandle.dump(obj)
    # current_app.logger.info(f"load_data:{ingrd_name_data}")
    # return jsonify(ingrd_name_data), 201
    # return {
    #     "status":"ok",
    #     "message":"added successfully",
    #     "data":ingrd_name_data
    # }

    # return objs
# class IngredientNameResouce(MethodResource):
    
#     @marshal_with(IngredienNameSchema(many=True))
#     def get(self):
#             """
#         Get list of ingredientName that meet with query filter given in paramters
#         ---
#         tags:
#         - ingredientName
#         description: Parameters can be provided in the query to search for ingredient name
#         operationId: get_ingredient_name
#         parameters:
#           - name: id
#             in: query
#             required: false
#             schema:
#             type: int
#           - name: name
#             in: query
#             required: false
#             schema:
#               type: string

#         responses:
#             '200':
#               description: ingredientNames to be returned
#               content:
#                 application/json:
#                   schema:
#                     type: array
#                     items:
#                       $ref: '#/components/schemas/ingredientName'
#         """
#         filters = request.args
#         objs = apiHandle.get_many(**filters)

#         return objs

#     @use_kwargs(IngredienNameSchema)
#     @marshal_with(IngredienNameSchema, code=201)
#     def post(self):
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({"status":"fail", "messagge":"recive empty body"}),400

#         load_data = apiHandle.load(json_data)
#         current_app.logger.info(f"data to post:{load_data}")
#         isExist = apiHandle.get(name=load_data["name"])
#         if isExist:
#             return abort(400,"IngredientName:{} already exist".format(load_data["name"]))
#         apiHandle.post(load_data)   
#         obj = IngredientName(**load_data)
#         ingrd_name_data = apiHandle.dump(obj)
#         current_app.logger.info(f"load_data:{ingrd_name_data}")
#         return {
#             "status":"ok",
#             "message":"added successfully",
#             "data":ingrd_name_data
#         }
        

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

