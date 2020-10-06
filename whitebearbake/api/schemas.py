import collections
import json

from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, validates_schema, ValidationError, pre_load, post_load,post_dump

from whitebearbake.database import db
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


# ======================== IngredientName section ========================

class IngredientNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName

class IngredientNameSchemaPOST(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName
        exclude = ('id',)

class jSendIngredientNameSchema(jSendSchema):
    data = fields.Nested('IngredientNameSchema', many=False,
                             required=True, description='IngredientName object, singular')

class jSendIngredientNamesSchema(jSendSchema):
    data = fields.Nested('IngredientNameSchema', many=True,
                             required=True, description='IngredientName object, Many')


# ======================== IngredientUnit section ========================          

class IngredientUnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientUnit

class IngredientUnitSchemaPOST(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientUnit
        exclude = ('id',)

class jSendIngredientUnitSchema(jSendSchema):
    data = fields.Nested('IngredientUnitSchema', many=False,
                             required=True, description='IngredientName object, singular')

class jSendIngredientUnitsSchema(jSendSchema):
    data = fields.Nested('IngredientUnitSchema', many=True,
                             required=True, description='IngredientName object, Many')

# ======================== Ingredient section ========================     

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    unit = fields.String(required=True)
    class Meta:
        model = Ingredient
        
class IngredientLoadInstSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(required=True)
    class Meta:
        model = Ingredient
        sqla_session = db.session
        fields = ('id',)
        load_instance = True

class IngredientSchemaNESTED(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    unit = fields.String(required=True)
    class Meta:
        model = Ingredient 
        exclude = ('id',)


class IngredientSchemaPOST(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, load_only=True)
    unit = fields.String(required=True, load_only=True)
    ingredientName_rel = fields.Nested('IngredientNameSchema', dump_only=True)
    ingredientUnit_rel = fields.Nested('IngredientUnitSchema', dump_only=True)

    class Meta:
        model = Ingredient    

    @post_load
    def get_name_unit(self, data, **kwags):
        ingredient_name = data.get("name", None) 
        if ingredient_name:
            data["ingredientName_rel"] = IngredientName.query.filter_by(name=ingredient_name).first() or IngredientName(name=ingredient_name)
        ingredient_unit = data.get("unit", None) 
        if ingredient_unit:
            data["ingredientUnit_rel"] = IngredientUnit.query.filter_by(name=ingredient_unit).first() or IngredientUnit(name=ingredient_unit)
        return data


            

                

class jSendIngredientSchema(jSendSchema):
    data = fields.Nested('IngredientSchema', many=False,
                             required=True, description='Ingredient object, singular')

class jSendIngredientsSchema(jSendSchema):
    data = fields.Nested('IngredientSchema', many=True,
                             required=True, description='Ingredient object, Many')

# ======================== Component section ========================

class ComponentSchema(ma.SQLAlchemyAutoSchema):
    ingredients = fields.Nested('IngredientSchemaNESTED', many=True)
    class Meta:
        model = Component
        # fields = ('id','name','instuction_list','ingredient_amount','ingredients','isRequire')

class ComponentSchemaPOST(ma.SQLAlchemyAutoSchema):
    ingredients = fields.Nested('IngredientLoadInstSchema', many=True)
    class Meta:
        model = Component
        exclude = ('id',)
        

class jSendComponentSchema(jSendSchema):
    data = fields.Nested('ComponentSchema', many=False,
                             required=True, description='Component object, singular')

class jSendComponentsSchema(jSendSchema):
    data = fields.Nested('ComponentSchema', many=True,
                             required=True, description='Component object, Many')
                    
# ======================== Baker section ========================

# recipe display for baker
class RecipeSchemaNESTED(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        fields = ('name',)

class RecipeLoadInstSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        sqla_session = db.session
        fields = ('id',)
        load_instance = True

class BakerSchema(ma.SQLAlchemyAutoSchema):
    recipes = fields.Nested('RecipeSchemaNESTED', many=True)
    class Meta:
        model = Baker
        # fields = ('id','name','instuction_list','ingredient_amount','ingredients','isRequire')

class BakerSchemaPOST(ma.SQLAlchemyAutoSchema):
    recipes = fields.Nested('RecipeLoadInstSchema', many=True)
    class Meta:
        model = Baker
        exclude = ('id',)

class BakerLoadInstSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Baker
        sqla_session = db.session
        fields = ('id',)
        load_instance = True

class BakerSchemaNESTED(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Baker
        fields = ('name',)
        

class jSendBakerSchema(jSendSchema):
    data = fields.Nested('BakerSchema', many=False,
                             required=True, description='Baker object, singular')

class jSendBakersSchema(jSendSchema):
    data = fields.Nested('BakerSchema', many=True,
                             required=True, description='Baker object, Many') 

# ======================== RecpImage section ========================
class RecpImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecpImage

class RecpImageSchemaPOST(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecpImage
        exclude = ('id',)

class RecpImageLoadInstSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecpImage
        sqla_session = db.session
        fields = ('id',)
        load_instance = True

class jSendRecpImageSchema(jSendSchema):
    data = fields.Nested('RecpImageSchema', many=False,
                             required=True, description='RecpImage object, singular')

class jSendRecpImagesSchema(jSendSchema):
    data = fields.Nested('RecpImageSchema', many=True,
                             required=True, description='RecpImage object, Many')

class RecpImageSchemaNESTED(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecpImage
        fields = ('image_link',)

# ======================== Recipe section ========================
# class RecipeSchemaNESTED(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Recipe
#         fields = ('name',)

# class RecipeLoadInstSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Recipe
#         sqla_session = db.session
#         fields = ('id',)
#         load_instance = True

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    baker = fields.Nested('RecipeSchemaNESTED', many=False)
    img = fields.Nested('IngredientSchema', many=False)
    class Meta:
        model = Recipe
        # fields = ('id','name','instuction_list','ingredient_amount','ingredients','isRequire')

class RecipeSchemaPOST(ma.SQLAlchemyAutoSchema):
    baker = fields.Nested('BakerLoadInstSchema', many=False)
    img = fields.Nested('RecpImageLoadInstSchema', many=False)
    class Meta:
        model = Recipe
        exclude = ('id',)
        

class jSendRecipeSchema(jSendSchema):
    data = fields.Nested('RecipeSchema', many=False,
                             required=True, description='Recipe object, singular')

class jSendRecipesSchema(jSendSchema):
    data = fields.Nested('RecipeSchema', many=True,
                             required=True, description='Recipe object, Many')
