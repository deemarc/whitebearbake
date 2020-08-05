import sys
from flask import abort, current_app
import sqlalchemy
from marshmallow import ValidationError
from whitebearbake.database import db

class Restive():
    """ Provides CRUD methods for Restful API endpoints """
    def __init__(self, resource, schema):
        """ Constructor """
        self._resource = resource
        self._schema = schema


    def dump(self, obj, many=False):
        """ RESTful Marshmallow serialization of object """
        
        try:
            data = self._schema().dump(obj, many=many)
        except ValidationError as error:
            errMsg = {
                "errorType":"Schema Dump ValidationError",
                "errMsg":error.messages
            }
            abort(400, errMsg)
        except :
            abort(400, "schema dump error with unknown reason")
            
        return data


    def load(self, json, many=False, partial=False):
        """ RESTful Marshmallow deserialization """
        try:
            data = self._schema().load(json, many=many, partial=partial)
        except ValidationError as error:
            errMsg = {
                "errorType":"Schema Load ValidationError",
                "errMsg":error.messages
            }
            abort(400, errMsg)
        except :
            abort(400, "schema load error with unknown reason")

        return data

    def get(self, id):
        """ Get record for a given resource """
        obj = self._resource.get(id)
        return obj

    def get_many(self, **kwargs):
        """ Gets zero or more records for a given resource """
        try:
            obj = self._resource.query.filter_by(**kwargs)
        except ValueError as err:
            current_app.logger.error(err)
            abort(400, err.args)
        return obj

    def post(self, data, attempts=1):
        """ Creates a new record from POST'd JSON """
        for attempt in range(attempts):
            try:
                obj = self._resource(**data)
                db.session.add(obj)
                db.session.commit()
                return obj
            except sqlalchemy.exc.IntegrityError as err:
                if attempt == attempts-1:
                    abort(409, ['A conflict happened while processing the request.', err.orig.__str__().strip()])
                continue

    def delete(self, id, attempts=1):
        """ Deletes an existing record """
        obj = self._resource.get(id) or abort(404)
        if not obj:
            return False
        for attempt in range(attempts):
            try:
                obj.delete()
                return True
            except sqlalchemy.exc.IntegrityError as err:
                if attempt == attempts-1:
                    abort(409, ['A conflict happened while processing the request.', err.orig.__str__().strip()])
                continue