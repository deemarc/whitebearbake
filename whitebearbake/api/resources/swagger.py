# Module imports
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import current_app


# App imports
from whitebearbake.api import bp
from whitebearbake.config import config
from whitebearbake.api.resources.ingredientNameResouce import *
from whitebearbake.api.schemas.schemas import IngredienNameSchema


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

    # add definition
    spec.components.schema("IngredienName", schema=IngredienNameSchema)

    return spec.to_dict()
