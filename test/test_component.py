import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from whitebearbake import create_app
from whitebearbake.database.models import *
from whitebearbake.database.models import db
from whitebearbake.api.schemas import IngredientSchemaPOST

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
    return obj.id
    
def getIngredient_list(dataList):
    output_list = []
    for item in dataList:
        cur_output = {'id':getIngredient(item)}
        output_list.append(cur_output)
    return output_list
    

class ComponentTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.apiRoot = '/api'
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        self.db.session.close()
        self.db.session.remove()

    """
    Testing ingredinetName endpoint
    """
    def test_get_component(self):
        # print("****** runtest test_get_questions")
        """Tests getting ingredient"""

        # get response and load data
        response = self.client().get(self.apiRoot + '/components')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_post_component_no_data(self):
        response = self.client().post(self.apiRoot + '/components')

        # check status code and message
        self.assertEqual(response.status_code, 400)

    def test_get_component_not_found(self):
        response = self.client().post(self.apiRoot + '/components/0')

        # check status code and message
        self.assertEqual(response.status_code, 404)

    def test_crud_ingredinet(self):
        """ Test whole sequence post patch delete ingredient
        and use get to verfy each step """
        ingredient_amount = [100, 5]
        
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
                
        instuction_list = ["prepare all ingredient","warm up milk", "mix in tea", "stir together"]
        postName = "a cub of milk tea"
        data = {}
        data["ingredient_amount"] = ingredient_amount
        ingredients_list = getIngredient_list(ingredients)
        self.app.logger.debug(f"ingredients_list:{ingredients_list}")
        data["ingredients"] = ingredients_list
        data["instuction_list"] = instuction_list
        data["name"] = postName
        self.app.logger.debug(f"data to post:{data}")
        response = self.client().post(self.apiRoot + '/components', json=data)
        data = json.loads(response.data)
        self.app.logger.debug(f"data:{data}")
        self.assertIn(response.status_code,[200,201])
        itemId = (data['data']).get('id',0)

        # === get id to see if its exist ===
        response = self.client().get(self.apiRoot + '/components/' + f'{itemId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual((data['data']).get('name','inValid'),postName)
        # check the len of instuction_list
        recp_ingredient_list  = (data['data']).get('ingredients',[])
        self.app.logger.debug(f"recp_ingredient_list:{recp_ingredient_list}")
        self.assertEqual(len(recp_ingredient_list),len(ingredients))
        


        # === patch ingredient ===
        data = {}
        patchIngredient = {'name':'dummyNameC','unit':'dummyUnitC'} 
        ingredients.append(patchIngredient)
        ingredient_amount.append(2)
        data["ingredient_amount"] = ingredient_amount
        data["ingredients"] = getIngredient_list(ingredients)

        # fullUrl = self.apiRoot + '/components/'+ f'{postName}'
        # self.app.logger.debug(f"fullUrl:{fullUrl}")
        response = self.client().patch(self.apiRoot + '/components/' + f'{itemId}', json=data)
        data = json.loads(response.data)
        # response = self.client().patch(fullUrl,data)
        self.app.logger.debug(f"reponse:{data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        # verify that new name is updated in the database
        self.assertEqual((data['data']).get('name','inValid'),postName)
        # check the len of instuction_list
        self.assertEqual(len((data['data']).get('ingredients',[])),len(ingredients))

        # === delete ingredient ===
        response = self.client().delete(self.apiRoot + '/components/' + f'{itemId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        

        

        

        





    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()