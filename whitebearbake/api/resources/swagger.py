# Module imports
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app


# App imports
from whitebearbake.api import bp
from whitebearbake.config import config


from whitebearbake.api.resources.ingredientNameResouce import *
from whitebearbake.api.schemas import IngredienNameSchema, IngredienNameSchemaPOST, jSendIngredientNameSchema, jSendIngredientNamesSchema

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

    # Add all paths for blueprint to spec
    spec.path(view=get_ingredient_name_resource)
    spec.path(view=post_ingredient_name_resource)
    spec.path(view=get_single_ingredient_name_resource)
    spec.path(view=patch_single_ingredient_name_resource)
    spec.path(view=delete_single_ingredient_name_resource)


    
    # add definition
    spec.components.schema("IngredienName", schema=IngredienNameSchema)
    spec.components.schema("IngredienNameRequest", schema=IngredienNameSchemaPOST)
    spec.components.schema("jSendIngredientName", schema=jSendIngredientNameSchema)
    spec.components.schema("jSendIngredientNames", schema=jSendIngredientNamesSchema)

    return spec.to_dict()
