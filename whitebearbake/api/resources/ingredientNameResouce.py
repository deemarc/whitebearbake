from flask import request, abort
from flask_restful import Resource


class IngredientNameResouce(Resource):
    
    def get(self):
        return {"status":'ok'}

# for query single item using ingredient name
class IngredientNameSingle(Resource):
    def get(self,name):
        return {"status":"ok"}
