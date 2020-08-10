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

    def get(self, **kwargs):
        """ Get record for a given resource """
        try:
            obj = self._resource.query.filter_by(**kwargs).first()
        except ValueError as err:
            current_app.logger.error(err)
            abort(400, err.args)
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
    def patch(self, obj, data):
        try:
            for key, value in data.items():
                setattr(obj,key, value)
            db.session.add(obj)
            db.session.commit()
            return obj
        except ValueError as err:
            current_app.logger.error(err)
            abort(400, err.args)
        return obj

    def delete(self, obj, attempts=1):
        """ Deletes an existing record """
        # Delete object
        for attempt in range(attempts):
            try:
                db.session.delete(obj)
                db.session.commit()
                return {'message': 'No data', 'status_code': 200, 'status': 'success', 'data': 'Entity deleted successfully'}
            except sqlalchemy.exc.IntegrityError as err:
                if attempt == attempts-1:
                    abort(409, ['A conflict happened while processing the request.', err.orig.__str__().strip()])
                continue