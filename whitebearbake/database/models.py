from . import db
import datetime

Component_Ingredient = db.Table('Component_Ingredient',
    db.Column('component_id', db.Integer, db.ForeignKey('component.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class Baker(db.Model):
    __tablename__ = 'baker'

    id = db.Column(db.Integer, primary_key=True)
    name = db.String(60, unique=True, nullable=False)
    description = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    youtube_linke = db.Column(db.String(120))
    phone = db.Column(db.String(120))

class Component(db.Model):
    __tablename__ = 'component'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True,nullable=False)
    instuction_list = db.Column(db.ARRAY(db.String), default=[])
    ingredient_amount = db.Column(db.ARRAY(db.Integer), default=[])
    ingredients = db.relationship('Ingredient', secondary=Component_Ingredient, lazy='joined')
    isRequire = db.Colomn(db.Boolean,default=True)

class IngredientName(db.Model):
    __tablename__ = 'ingredientname'
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(60,nullable=False,unique=True)


class IngredientUnit(db.Model):
    __tablename__ = 'ingredientunit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(60,nullable=False,unique=True)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    name_id = db.Column(db.Integer, db.ForeignKey('Ingredient_Name.id'),nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('Ingredient_Unit.id'),nullable=False)
    description = db.String(200)
    components = db.relationship('Component', secondary=Component_Ingredient, lazy='joined')
    
class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)



class RecpImage():
    # it is and actual item store not and intermediate table for many-to-many relationship
    # so, it decide to use camel case
    __tablename__= 'recpimage'

    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(200))

