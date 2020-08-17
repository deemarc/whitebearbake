import collections
import json

from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validates_schema, ValidationError, pre_load

from whitebearbake.database.models import *


ma = Marshmallow()

class JSONField(fields.Field):
    """ A JSON field. Supports dicts and dict-like objects. """
    default_error_messages = {'invalid': 'Not a valid JSON object.'}

    def _serialize(self, value, attr, data):
        """ Load json to obj """
        return json.loads(value) if value else None

    def _deserialize(self, value, attr, data):
        """ Dumps json from obj """
        if isinstance(value, collections.Mapping):
            return json.dumps(value)
        else:
            self.fail('invalid')


class JSONSchema(Schema):
    """ Custom JSON schema class"""
    @validates_schema(pass_original=True)
    def validate_object(self, data, original_data):
        """Checks input data for extraneous fields"""
        for key in original_data:
            if key not in self.fields:
                raise ValidationError('Unknown field name {}'.format(key))

    def dump_json(self, obj):
        """ Dumps JSON """
        return json.dumps(obj)

    def load_json(self, value):
        """ Loads JSON """
        return str(value)

class jSendSchema(ma.Schema):
    """ jSend wrapper schema """
    data = fields.Dict(required=True, description='jSend payload')
    message = fields.Str(required=True, description='jSend message')
    status = fields.Str(required=True, description='jSend status')
    status_code = fields.Integer(required=True, description='HTTP status code returned outside of the headers')
    timestamp = fields.DateTime(required=True, description='Timestamp of the request')
    uuid = fields.UUID(required=True, description='UUID for the request, used for logging/debugging')

class IngredienNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName

class IngredienNameSchemaPOST(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName
        exclude = ('id',)

class jSendIngredientNameSchema(jSendSchema):
    data = fields.Nested('InformationSchema', many=False,
                             required=True, description='IngredientName object, singular')

class jSendIngredientNamesSchema(jSendSchema):
    data = fields.Nested('InformationSchema', many=True,
                             required=True, description='IngredientName object, Many')