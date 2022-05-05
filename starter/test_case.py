import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Post, Reply

ADMINISTRATOR = os.environ.get('ADMINISTRATOR')
REGISTED_VISITOR = os.environ.get['REGISTED_VISITOR']

class ForumTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "boardgame_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_posts(self):
        res = self.client().get('/posts')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_posts'])
        self.assertTrue(len(data['posts']))

    def test_404_retrieve_posts(self):
        res = self.client().get('/post')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


    def test_create_post(self):
        res = self.client().post('/posts', headers={'Authorization': "Bearer "+ADMINISTRATOR}, json={'subject':  'Ark Nova is a great game','content':  'Everyone love to build zoo!'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_401_creat_post(self):
        res = self.client().post('/posts', json={'subject':  'Ark Nova is a great game','content':  'Everyone love to build zoo!'})

        self.assertEqual(res.status_code, 401)

    def test_delete_specific_post(self):
        res = self.client().delete('/posts/1', headers={'Authorization': "Bearer "+ADMINISTRATOR})
        data = json.loads(res.data)

        post = Post.query.filter(Post.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(post, None)
        

    def test_404_delete_specific_post(self):
        res = self.client().delete('/posts/1000', headers={'Authorization': "Bearer "+ADMINISTRATOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_specific_post(self):
        res = self.client().patch('/posts/2', json={'subject':  'Redland is a great two player game','content':  'I think 7 wonders duel better!'}, headers={'Authorization': "Bearer "+REGISTED_VISITOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated'], 2)
        self.assertEqual(data['success'], True)
        

    def test_403_update_specific_post(self):
        res = self.client().patch('/posts/2', json={'subject':  'Redland is a great two player game','content':  'I think 7 wonders duel better!'}, headers={'Authorization': "Bearer "+ADMINISTRATOR})

        self.assertEqual(res.status_code, 403)

    def test_get_specific_post(self):
        res = self.client().get('/posts/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['subject'])
        self.assertTrue(data['content'])
        self.assertTrue(data['total_replies'])

    def test_404_get_specific_post(self):
        res = self.client().get('/posts/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_reply(self):
        res = self.client().post('/posts/5',  json={"reply":"I think 7 wonders duel better!"}, headers={'Authorization': "Bearer "+REGISTED_VISITOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_401_creat_reply(self):
        res = self.client().post('/posts/3', json={'reply':  'The box is so huge!'})

        self.assertEqual(res.status_code, 401)
    
    def test_delete_specific_reply(self):
        res = self.client().delete('/replies/6', headers={'Authorization': "Bearer "+ADMINISTRATOR})
        data = json.loads(res.data)

        reply = Reply.query.filter(Reply.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        self.assertEqual(reply, None)
        

    def test_404_delete_specific_reply(self):
        res = self.client().delete('/replies/1000', headers={'Authorization': "Bearer "+ADMINISTRATOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search_posts(self):
        res = self.client().post('/posts/result', json={'searchTerm': 'game'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalPosts'])
        self.assertTrue(len(data['posts']))

    def test_no_result_search_posts(self):
        res = self.client().post('/posts/result', json={'searchTerm': 'none exist question bla bla bla'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['totalPosts'])
        self.assertFalse(len(data['posts']))

    def test_400_search_posts(self):
        res = self.client().post('/posts/result')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()