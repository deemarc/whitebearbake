from whitebearbake.api.schemas import ma
from whitebearbake.database.models import *
class IngredienNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName

    
    