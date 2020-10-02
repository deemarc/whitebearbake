# import flask package
from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with
from flask_apispec.views import MethodResource

# import inside the package
from whitebearbake.api import bp
from whitebearbake.api.resources.masqlapi import masqlapi
from whitebearbake.api.schemas import RecipeSchema, RecipeSchemaPOST
from whitebearbake.api.decorators import jSend

from whitebearbake.database import db
from whitebearbake.database.models import Recipe



apiHandle = masqlapi(db.session, Recipe ,RecipeSchema, RecipeSchemaPOST)

@bp.route('/recipes', methods=['GET'])
@jSend
def get_recipe_resource():
    """
    Get list of recipe that meet with query filter given in paramters
    ---
    get:
        description: Parameters can be provided in the query to search for recipe 
        operationId: get_recipe
        tags:
         - recipe
        parameters:
          - name: id
            in: query
            required: false
            description: recipe resource identifier
            schema:
              type: int
          - name: name
            in: query
            description: recipe's Name
            required: false
            schema:
              type: string
        responses:
            200:
                description: recipes to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecipes"
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

@bp.route('/recipes', methods=['POST'])
@jSend
def post_recipe_resource():
    """
    Create new recipe with given parameter inside request body
    ---
    post:
        description: Create new recipe with given parameter inside request body
        operationId: post_recipe
        tags:
         - recipe
        responses:
            201:
                description: return recipe item when it was successfully created
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecipes"
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
                $ref: "#/components/schemas/RecipeSchemaPOST"
              
    """
    return apiHandle.post("name")
        
@bp.route('/recipes/<id>', methods=['GET'])
@jSend
def get_single_recipe_resource(name):
    """
    Get specific recipe by the id
    ---
    get:
        description: Get specific recipe
        operationId: get_single_recipe
        tags:
         - recipe
        parameters:
          - name: id
            in: path
            description: recipe's id
            required: true
            schema:
              type: int
            
        responses:
            200:
                description: recipes to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecipe"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(name=name) or abort(404)
    return apiHandle.getMethod(obj)

@bp.route('/recipes/<id>', methods=['PATCH'])
@jSend
def patch_single_recipe_resource(id):
    """
    Modifies specific recipe by the id
    ---
    patch:
        description: Modifies specific recipe
        operationId: patch_single_recipe
        tags:
         - recipe
        parameters:
          - name: id
            in: path
            description: recipe's id
            required: true
            schema:
              type: int
        requestBody:
          description: Action payload
          required: true
          content:
            application/json:
              schema: 
                $ref: "#/components/schemas/RecipeSchemaPOST"
        responses:
            200:
                description: recipes to be returned
                content:
                  application/json:
                    schema:
                      $ref: "#/components/schemas/jSendRecipe"
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.patch(obj)

@bp.route('/recipes/<id>', methods=['DELETE'])
@jSend
def delete_single_recipe_resource(id):
    """
    delete specific recipe by the id
    ---
    delete:
        description: Delete specific recipe
        operationId: delete_single_recipe
        tags:
         - recipe
        parameters:
          - name: id
            in: path
            description: recipe's id
            required: true
            schema:
              type: string
        responses:
            200:
                description: successfully deleted recipes entity
            400:
                description: Bad Request
            429:
                description: Too Many Requests
            500:
                description: Internal Server Error
    """
    obj = apiHandle.get(id=id) or abort(404)
    return apiHandle.delete(obj)