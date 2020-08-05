from flask import request, abort, jsonify, current_app
from flask_restful import Resource
from whitebearbake.api.schemas.schemas import IngredientSchema
from whitebearbake.database import db
from whitebearbake.database.models import IngredientName
from whitebearbake.api.apierror import ApiError


class IngredientNameResouce(Resource):
    
    def get(self):
        # return {"status":'ok'}
        raise ValueError("test exception")
    
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({"status":"fail", "messagge":"recive empty body"}),400

        load_data = IngredientSchema().load(json_data)
        current_app.logger.info(f"data to post:{load_data}")
        isExist = IngredientName.query.filter_by(name=load_data["name"]).first()
        IngredientName.query.filter_by(name="milk").first()
        if isExist:
            return abort(400,"IngredientName:{} already exist".format(load_data["name"]))
        ingrd_name = IngredientName(**load_data)
        db.session.add(ingrd_name)
        db.session.commit()
        ingrd_name_data = IngredientSchema().dump(ingrd_name)
        current_app.logger.info(f"load_data:{ingrd_name_data}")
        return {
            "status":"ok",
            "message":"added successfully",
            "data":ingrd_name_data
        }



        

        

# for query single item using ingredient name
class IngredientNameSingle(Resource):
    def get(self,name):
        return {"status":"ok"}
