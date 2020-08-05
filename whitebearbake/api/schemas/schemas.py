from whitebearbake.api.schemas import ma
from whitebearbake.database.models import *
class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IngredientName

    
    