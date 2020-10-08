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


class RecpImagesTestCase(unittest.TestCase):
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

            # add one recpImage
            data = {}
            image_link = "http://localhost/dummy.jpg"
            data["image_link"] = image_link
            obj = RecpImage.query.filter_by(image_link=image_link).first()
            if not obj:
                obj = RecpImage(**data)
                db.session.add(obj)
                db.session.commit()
            
            
    
    def tearDown(self):
        """Executed after reach test"""
        self.db.session.close()
        self.db.session.remove()

    """
    Testing RecpImage endpoint
    """
    def test_get_recpimage(self):
        # print("****** runtest test_get_questions")
        """Tests getting recpimage"""

        # get response and load data
        response = self.client().get(self.apiRoot + '/recpimages')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_post_recpimage_no_data(self):
        response = self.client().post(self.apiRoot + '/recpimages')

        # check status code and message
        self.assertEqual(response.status_code, 400)

    def test_get_recpimage_not_found(self):
        response = self.client().post(self.apiRoot + '/recpimages/0')

        # check status code and message
        self.assertEqual(response.status_code, 404)

    def test_crud_recpimage(self):
        """ Test whole sequence post patch delete recpimage
        and use get to verfy each step """
        image_link = "http://localhost/whitebearbake.jpg"
        image_link_patch = "http://localhost/whitebearbakebake.jpg"       
        data = {}
        data["image_link"] = image_link
        response = self.client().post(self.apiRoot + '/recpimages', json=data)
        data = json.loads(response.data)
        self.assertIn(response.status_code,[200,201])
        itemId = (data['data']).get('id',0)

        # === get id to see if its exist ===
        response = self.client().get(self.apiRoot + '/recpimages/' + f'{itemId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual((data['data']).get('image_link','inValid'),image_link)

        # === patch recpimage ===
        data = {}
        data["image_link"] = image_link_patch

        # fullUrl = self.apiRoot + '/recpimages/'+ f'{postName}'
        # self.app.logger.debug(f"fullUrl:{fullUrl}")
        response = self.client().patch(self.apiRoot + '/recpimages/' + f'{itemId}', json=data)
        data = json.loads(response.data)
        # response = self.client().patch(fullUrl,data)
        self.app.logger.debug(f"reponse:{data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        # verify that new name is updated in the database
        self.assertEqual((data['data']).get('image_link','inValid'),image_link_patch)

        # === delete recpimage ===
        response = self.client().delete(self.apiRoot + '/recpimages/' + f'{itemId}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        

        

        

        





    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()