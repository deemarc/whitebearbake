# Module imports
from flask import request, abort, current_app
from sqlalchemy import exc
from marshmallow import ValidationError


class masqlapi():
    """ RestfulAPI SQLA/MarshMallow/jSend class """

    def __init__(self, session, resource, roschema, rwschema):
        """ Constructor """
        self.session = session
        self.resource = resource
        self.roschema = roschema
        self.rwschema = rwschema

    def get(self, **kwargs):
        """ Get record for a given resource """
        try:
            current_app.logger.debug(f'kwargs:{kwargs}')
            obj = self.resource.query.filter_by(**kwargs).first()
        except ValueError as err:
            current_app.logger.error(err)
            abort(400, err.args)
        return obj

    def get_many(self, **kwargs):
        """ Gets zero or more records for a given resource """
        try:
            obj = self.resource.query.filter_by(**kwargs)
        except ValueError as err:
            current_app.logger.error(err)
            abort(400, err.args)
        return obj

    def getMethod(self, obj, many=False):
        """ GET one """
        # Dump object
        try:
            data = self.roschema().dump(obj, many=many)
        except ValidationError as error:
            errMsg = {
                "errorType":"Schema Dump ValidationError",
                "errMsg":error.messages
            }
            abort(400, errMsg)
        except :
            abort(500, "schema dump error with unknown reason")

       
        # Return entity
        return {'message': None, 'status_code': 200, 'status': 'success', 'data': data}


    def patch(self, obj):
        """ PATCH """
        # Grab request data
        json = request.get_json()
        if not json:
            return {'message': 'Bad request', 'status_code': 400, 'status': 'failure', 'data': 'JSON input object is missing or cannot be parsed'}
        
        try:
            # data = self.rwschema().load(json, instance=obj, partial=True)
            data = self.rwschema().dump(obj)
            patch_data = self.rwschema().load(json, partial=True)
            data.update(patch_data)

            current_app.logger.debug(f"data for patching:{data}")
        except ValidationError as error:
            errMsg = {
                "errorType":"Schema Load ValidationError",
                "errMsg":error.messages
            }
            abort(400, errMsg)
        except :
            abort(500, "schema load error with unknown reason")

        # Merge and Commit
        try:
            for key, value in data.items():
                setattr(obj,key, value)
            self.session.add(obj)
            self.session.commit()
            data = self.roschema().dump(obj)
            return {'message': 'OK - entity updated successfully', 'status_code': 200, 'status': 'success', 'data': data}
        except exc.IntegrityError as err:
            self.session.rollback()
            return {'message': 'Conflict', 'status_code': 409, 'status': 'failure', 'data': err.orig.__str__().strip()}
        except Exception as err:
            self.session.rollback()
            raise err


    def delete(self, obj):
        """ DELETE """
        # Delete object
        try:
            self.session.delete(obj)
            self.session.commit()
            return {'message': 'No data', 'status_code': 200, 'status': 'success', 'data': 'Entity deleted successfully'}
        except exc.IntegrityError as err:
            self.session.rollback()
            return {'message': 'Conflict', 'status_code': 409, 'status': 'failure', 'data': err.orig.__str__().strip()}
        except Exception as err:
            self.session.rollback()
            raise err


    def post(self,uniqueField):
        """ POST """

        # if uniqueField is not a list we make it into one
        if not isinstance(uniqueField, list):
            uniqueField_list = [uniqueField]
        else:
            uniqueField_list = uniqueField
        # Grab request data
        json = request.get_json()
        if not json:
            return {'message': 'Bad request', 'status_code': 400, 'status': 'failure', 'data': 'JSON input object is missing or cannot be parsed'}
        # print("json:{0}, type:{1}".format(json,type(json)))
        # Validate and deserialize input
        try:
            data = self.rwschema().load(json)
        except ValidationError as error:
            errMsg = {
                "errorType":"Schema Load ValidationError",
                "errMsg":error.messages
            }
            abort(400, errMsg)
        except :
            abort(500, "schema load error with unknown reason")
            
        query = {}
        for keys in uniqueField_list:
            query[keys] = data[keys]
        # Check for existing row based on passed JSON
        current_app.logger.info(f"query data in post function:{query}")
        existing = self.resource.query.filter_by(**query).first()

        if existing:
            obj=self.roschema().dump(existing)
            return {'message': 'OK - entity exists', 'status_code': 200, 'status': 'success', 'data': obj}

        # Add and Commit
        try:
            obj = self.resource(**data)
            self.session.add(obj)
            self.session.commit()
            data = self.roschema().dump(obj)
            return {'message': 'Created - entity created successfully', 'status_code': 201, 'status': 'success', 'data': data}
        except exc.IntegrityError as err:
            self.session.rollback()
            return {'message': 'Conflict', 'status_code': 409, 'status': 'failure', 'data': err.orig.__str__().strip()}
        except Exception as err:
            self.session.rollback()
            raise err
