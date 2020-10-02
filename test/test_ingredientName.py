import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from whitebearbake import create_app
from whitebearbake.database.models import *
from whitebearbake.database.models import db

# from database.models import *
# from models import setup_db, Question, Category
# from whitebearbake.models import db 


class IngredientNameTestCase(unittest.TestCase):
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
            # self.db.create_all()
            
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        self.db.session.close()
        self.db.session.remove()

    """
    Testing ingredinetName endpoint
    """
    def test_get_ingredientName(self):
        # print("****** runtest test_get_questions")
        """Tests getting ingredientName"""

        # get response and load data
        response = self.client().get(self.apiRoot + '/ingredientNames')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_post_ingredientName_no_data(self):
        response = self.client().post(self.apiRoot + '/ingredientNames')

        # check status code and message
        self.assertEqual(response.status_code, 400)

    def test_get_ingredientName_not_found(self):
        response = self.client().post(self.apiRoot + '/ingredientNames/0')

        # check status code and message
        self.assertEqual(response.status_code, 404)

    def test_crud_ingredinetName(self):
        """ Test whole sequence post patch delete ingredientName
        and use get to verfy each step """
        postName = "oreo"
        patchName = "oreo2"
        data = {}
        data["name"] = postName
        response = self.client().post(self.apiRoot + '/ingredientNames', json=data)
        data = json.loads(response.data)

        self.assertIn(response.status_code,[200,201])
        # self.app.logger.debug(f'/ingredientNames/{itemName}')
        # === get id to see if its exist ===
        response = self.client().get(self.apiRoot + '/ingredientNames/' + f'{postName}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual((data['data']).get('name','inValid'),postName)

        # === patch ingredientName ===
        data = {}
        data['name'] = patchName
        # fullUrl = self.apiRoot + '/ingredientNames/'+ f'{postName}'
        # self.app.logger.debug(f"fullUrl:{fullUrl}")
        response = self.client().patch(self.apiRoot + '/ingredientNames/' + f'{postName}', json=data)
        data = json.loads(response.data)
        # response = self.client().patch(fullUrl,data)
        self.app.logger.debug(f"reponse:{data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        # verify that new name is updated in the database
        self.assertEqual((data['data']).get('name','inValid'),patchName)

        # === delete ingredientName ===
        response = self.client().delete(self.apiRoot + '/ingredientNames/' + f'{patchName}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        

        

        

        





    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()