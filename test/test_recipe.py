import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from whitebearbake import create_app
from whitebearbake.database.models import *
from whitebearbake.database.models import db
from whitebearbake.api.schemas import *

# from whitebearbake.api.schemas import IngredientSchemaPOST

# from database.models import *
# from models import setup_db, Question, Category
# from whitebearbake.models import db 
def getIngredient(dataDict):
    # if ingredient exist return id
    # if not create it and return newly create id

    obj = Ingredient.query.filter_by(**dataDict).first()
    if not obj:
        data = IngredientSchemaPOST().load(dataDict)
        obj = Ingredient(**data)
        db.session.add(obj)
        db.session.commit()
    return obj
    
def getIngredient_list(dataList):
    output_list = []
    for item in dataList:
        cur_output = getIngredient(item)
        output_list.append(cur_output)
    return output_list

class RecipeTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.apiRoot = '/api'
        self.baker_name = 'whitebearbake'
        self.component_name = "a cub of milk tea"
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            # make baker
            obj = Baker.query.filter_by(name=self.baker_name).first()
            if not obj:
                obj = Baker(name=self.baker_name)
                db.session.add(obj)
                db.session.commit()
            self.bake_id = obj.id

            # make Ingredient
            ingredients = [
                {
                    "name":"milk",
                    "unit":"ml"
                },
                {
                    "name":"tea",
                    "unit":"g"
                }
            ]
            data = {}
            data['ingredients'] = getIngredient_list(ingredients)
            data['instuction_list'] = ["prepare all ingredient","warm up milk", "mix in tea", "stir together"]
            data['name'] = self.component_name
            data["ingredient_amount"] = [100, 5]
            obj = Component.query.filter_by(name=self.component_name).first()
            if not obj:
                obj = Component(**data)
                db.session.add(obj)
                db.session.commit()
            self.component_id = obj.id
            
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        self.db.session.close()
        self.db.session.remove()

    """
    Testing ingredinetName endpoint
    """
    def test_get_recipe(self):
        # print("****** runtest test_get_questions")
        """Tests getting Recipe"""

        # get response and load data
        response = self.client().get(self.apiRoot + '/recipes')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_post_recipe_no_data(self):
        response = self.client().post(self.apiRoot + '/recipes')

        # check status code and message
        self.assertEqual(response.status_code, 400)

    def test_get_recipe_not_found(self):
        response = self.client().post(self.apiRoot + '/recipes/0')

        # check status code and message
        self.assertEqual(response.status_code, 404)

    def test_crud_recipe(self):
        """ Test whole sequence post patch delete Recipe
        and use get to verfy each step """
        postName = 'just milk tea recipe'
        patchName = 'patch milk tea recipe'
        data = {}
        data['name'] = postName
        data["baker"] = {
            'id':self.bake_id
        }
        data["components"] = [
            {
                'id':self.component_id
            }
        ]


        response = self.client().post(self.apiRoot + '/recipes', json=data)
        data = json.loads(response.data)
        self.assertIn(response.status_code,[200,201])
        itemId = (data['data']).get('id',0)

        # === get id to see if its exist ===
        response = self.client().get(self.apiRoot + '/recipes/' + f'{itemId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual((data['data']).get('name','inValid'),postName)
        # check the len of instuction_list
        recv_component_list = (data['data']).get('components',[])
        self.app.logger.debug(f"recv_component_list:{recv_component_list}")
        self.assertEqual(len(recv_component_list),1)
        
        # === patch ingredient ===
        data = {}
        data['name'] = patchName
        data["components"] = []

        response = self.client().patch(self.apiRoot + '/recipes/' + f'{itemId}', json=data)
        data = json.loads(response.data)
        # response = self.client().patch(fullUrl,data)
        self.app.logger.debug(f"reponse:{data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        # verify that new name is updated in the database

        # check the len of instuction_list
        recv_component_list = (data['data']).get('components',[])
        self.app.logger.debug(f"recv_component_list:{recv_component_list}")
        self.assertEqual(len((data['data']).get('components',[])),0)
        
        # === delete ingredient ===
        response = self.client().delete(self.apiRoot + '/recipes/' + f'{itemId}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        

        

        

        





    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()