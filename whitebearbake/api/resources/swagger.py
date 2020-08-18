# Module imports
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app


# App imports
from whitebearbake.api import bp
from whitebearbake.config import config


from whitebearbake.api.resources.ingredientNameResouce import *
from whitebearbake.api.resources.ingredientUnitResource import *
from whitebearbake.api.resources.ingredientResource import * 

from whitebearbake.api.schemas import *


@bp.route('/swagger.json', methods=['GET'])
def swagger():
    """ Returns swagger spec JSON """
    # Create an APISpec
    spec = APISpec(
        **config['APISPEC'],
        plugins=[FlaskPlugin(),
            MarshmallowPlugin()
        ],
        # version=config.get('APP_VERSION')
    )

    # === Add all paths for blueprint to spec

    # IngredientName
    spec.path(view=get_ingredient_name_resource)
    spec.path(view=post_ingredient_name_resource)
    spec.path(view=get_single_ingredient_name_resource)
    spec.path(view=patch_single_ingredient_name_resource)
    spec.path(view=delete_single_ingredient_name_resource)

    # IngredientUnit
    spec.path(view=get_ingredient_unit_resource)
    spec.path(view=post_ingredient_unit_resource)
    spec.path(view=get_single_ingredient_unit_resource)
    spec.path(view=patch_single_ingredient_unit_resource)
    spec.path(view=delete_single_ingredient_unit_resource)

    # Ingredient
    spec.path(view=get_ingredient_resource)
    spec.path(view=post_ingredient_resource)
    spec.path(view=get_single_ingredient_resource)
    spec.path(view=patch_single_ingredient_resource)
    spec.path(view=delete_single_ingredient_resource)

    
    # === add definition

    # IngredientName
    spec.components.schema("IngredientName", schema=IngredientNameSchema)
    spec.components.schema("IngredientNameSchemaPOST", schema=IngredientNameSchemaPOST)
    spec.components.schema("jSendIngredientName", schema=jSendIngredientNameSchema)
    spec.components.schema("jSendIngredientNames", schema=jSendIngredientNamesSchema)

    # IngredientUnit
    spec.components.schema("IngredientUnit", schema=IngredientUnitSchema)
    spec.components.schema("IngredientUnitSchemaPOST", schema=IngredientUnitSchemaPOST)
    spec.components.schema("jSendIngredientUnit", schema=jSendIngredientUnitSchema)
    spec.components.schema("jSendIngredientUnits", schema=jSendIngredientUnitsSchema)

    # Ingredient
    spec.components.schema("Ingredient", schema=IngredientSchema)
    spec.components.schema("IngredientSchemaPOST", schema=IngredientSchemaPOST)
    spec.components.schema("jSendIngredient", schema=jSendIngredientSchema)
    spec.components.schema("jSendIngredients", schema=jSendIngredientsSchema)

    return spec.to_dict()
