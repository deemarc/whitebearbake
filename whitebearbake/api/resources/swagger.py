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
from whitebearbake.api.resources.componentResource import *
from whitebearbake.api.resources.bakerResource import *
from whitebearbake.api.resources.recipeResource import *
from whitebearbake.api.resources.recpImageResource import *

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

    # Component
    spec.path(view=get_component_resource)
    spec.path(view=post_component_resource)
    spec.path(view=get_single_component_resource)
    spec.path(view=patch_single_component_resource)
    spec.path(view=delete_single_component_resource)

    # Baker
    spec.path(view=get_baker_resource)
    spec.path(view=post_baker_resource)
    spec.path(view=get_single_baker_resource)
    spec.path(view=patch_single_baker_resource)
    spec.path(view=delete_single_baker_resource)

    # Recipe
    spec.path(view=get_recipe_resource)
    spec.path(view=post_recipe_resource)
    spec.path(view=get_single_recipe_resource)
    spec.path(view=patch_single_recipe_resource)
    spec.path(view=delete_single_recipe_resource)

    # RecpImage
    spec.path(view=get_recpImage_resource)
    spec.path(view=post_recpImage_resource)
    spec.path(view=get_single_recpImage_resource)
    spec.path(view=patch_single_recpImage_resource)
    spec.path(view=delete_single_recpImage_resource)
    

    
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

    # Component
    spec.components.schema("Component", schema=ComponentSchema)
    spec.components.schema("ComponentSchemaPOST", schema=ComponentSchemaPOST)
    spec.components.schema("jSendComponent", schema=jSendComponentSchema)
    spec.components.schema("jSendComponents", schema=jSendComponentsSchema)

    # Baker
    spec.components.schema("Baker", schema=BakerSchema)
    spec.components.schema("BakerSchemaPOST", schema=BakerSchemaPOST)
    spec.components.schema("jSendBaker", schema=jSendBakerSchema)
    spec.components.schema("jSendBakers", schema=jSendComponentsSchema)

    # Recipe
    spec.components.schema("Recipe", schema=RecipeSchema)
    spec.components.schema("RecipeSchemaPOST", schema=RecipeSchemaPOST)
    spec.components.schema("jSendRecipe", schema=jSendRecipeSchema)
    spec.components.schema("jSendRecipes", schema=jSendComponentsSchema)

    # RecipeImage
    spec.components.schema("RecpImage", schema=RecpImageSchema)
    spec.components.schema("RecpImageSchemaPOST", schema=RecpImageSchemaPOST)
    spec.components.schema("jSendRecipeImage", schema=jSendRecpImageSchema)
    spec.components.schema("jSendRecipeImages", schema=jSendRecpImagesSchema)

    return spec.to_dict()
