from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from whitebearbake.api.schemas.schemas import IngredientSchema
from whitebearbake.database import db
from whitebearbake.database.models import IngredientName
from whitebearbake.api.apierror import ApiError
from whitebearbake.api.resources.restive import Restive

apiHandle = Restive(IngredientName,IngredientSchema)


class IngredientNameResouce(Resource):
    
    def get(self):
        filters = request.args
        objs = apiHandle.get_many(**filters)

        return apiHandle.dump(objs,many=True), 200
    
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({"status":"fail", "messagge":"recive empty body"}),400

        load_data = apiHandle.load(json_data)
        current_app.logger.info(f"data to post:{load_data}")
        isExist = apiHandle.get(name=load_data["name"])
        if isExist:
            return abort(400,"IngredientName:{} already exist".format(load_data["name"]))
        apiHandle.post(load_data)   
        obj = IngredientName(**load_data)
        ingrd_name_data = apiHandle.dump(obj)
        current_app.logger.info(f"load_data:{ingrd_name_data}")
        return {
            "status":"ok",
            "message":"added successfully",
            "data":ingrd_name_data
        }
        

# for query single item using ingredient name
class IngredientNameSingle(Resource):
    def get(self,name):
        obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")

        return apiHandle.dump(obj,many=False), 200 

    def patch(self,name):
        json_data = request.get_json()
        if not json_data:
            return jsonify({"status":"fail", "messagge":"recive empty body"}),400
        patch_data = apiHandle.load(json_data,partial=True)
        obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")
        obj = apiHandle.patch(obj,patch_data)
        return apiHandle.dump(obj,many=False), 200 

    def delete(self,o):
        obj = apiHandle.get(name=name) or abort(404,f"item with the name:{name}, doesn't exist")
        return apiHandle.delete(obj), 200

