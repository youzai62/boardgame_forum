import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Post, Reply


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
        res = self.client().post('/posts', headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"}, json={'subject':  'Ark Nova is a great game','content':  'Everyone love to build zoo!'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_401_creat_post(self):
        res = self.client().post('/posts', json={'subject':  'Ark Nova is a great game','content':  'Everyone love to build zoo!'})

        self.assertEqual(res.status_code, 401)

    def test_delete_specific_post(self):
        res = self.client().delete('/posts/1', headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})
        data = json.loads(res.data)

        post = Post.query.filter(Post.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(post, None)
        

    def test_404_delete_specific_post(self):
        res = self.client().delete('/posts/1000', headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_specific_post(self):
        res = self.client().patch('/posts/2', json={'subject':  'Redland is a great two player game','content':  'I think 7 wonders duel better!'}, headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNTdhZjIwZmMzZjk0MDA2ZWE2OTM0YSIsImF1ZCI6WyJib2FyZGdhbWVmb3J1bSIsImh0dHBzOi8vZGV2LXJveXpodS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjUxNTYyMzk4LCJleHAiOjE2NTE2NDg3OTgsImF6cCI6IndSSkVjQnk0NjZNUXg2VmVRenplbTFrU1lzM0N4cENHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbInBhdGNoOnBvc3RzIiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.CI_1Mm7paPVeL-_VKCSAnik3NlVc6B2XpiHVqiHcx8nJN1AkCkUaoH-0gu8YV-3G2HDSyyzyOcfc1velIknH2b_ttF2Kdi9sMSUKRC5BLFY1LtCfL-XntQETxrYNwxYodmtLhFlq8HJlwp0--pXVBOnyfWFsSPMogF-fIqgO-wFQaprAkyUgMDb3LnqkFFETYTJuHrkSg4E8NfHjTDgM4L8NphpKYR2Xj3MHiYXN4Ibgy1xXE1Gp5GcX-TDKIEX2iOyYCkJgGQux3VdElUE7z9EwjIdq2ASftRmtL8YaO8Z4AwRDZobM8uGU_r3TTwnYrj6NZ7JO8RiuDMG11vI9Vw"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated'], 2)
        self.assertEqual(data['success'], True)
        

    def test_403_update_specific_post(self):
        res = self.client().patch('/posts/2', json={'subject':  'Redland is a great two player game','content':  'I think 7 wonders duel better!'}, headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})

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
        res = self.client().post('/posts/5',  json={"reply":"I think 7 wonders duel better!"}, headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_401_creat_reply(self):
        res = self.client().post('/posts/3', json={'reply':  'The box is so huge!'})

        self.assertEqual(res.status_code, 401)
    
    def test_delete_specific_reply(self):
        res = self.client().delete('/replies/6', headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})
        data = json.loads(res.data)

        reply = Reply.query.filter(Reply.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        self.assertEqual(reply, None)
        

    def test_404_delete_specific_reply(self):
        res = self.client().delete('/replies/1000', headers={'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1oVHZHUlVKNWNRVnFrbTh2T3FzNSJ9.eyJpc3MiOiJodHRwczovL2Rldi1yb3l6aHUudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NjE5OTkwOTA1MjU4NzcwMjgzIiwiYXVkIjpbImJvYXJkZ2FtZWZvcnVtIiwiaHR0cHM6Ly9kZXYtcm95emh1LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NTE1NjA3NDMsImV4cCI6MTY1MTY0NzE0MywiYXpwIjoid1JKRWNCeTQ2Nk1ReDZWZVF6emVtMWtTWXMzQ3hwQ0ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3RzIiwiZGVsZXRlOnJlcGx5IiwicG9zdDpwb3N0cyIsInBvc3Q6cmVwbHkiXX0.oevsn0Hv28USqla1NfZuA1THm9cV1_c5zW9t2cLaQDbj9_VKaq-R6ebvickiQwkhacrvMn2asFTo-rOBavSMFmU77FeoMTZjKAx_B9XHbrtyAYV73IGOB1wawayGT_URU7WUSFJ6WGU5VEnUDGmDanhjrYAaB4iq9RujSveX550GL_sOYdsUQ2sOK35URM4F2mOkhFmxaSvL7JlzO7Zi1syf5AmXa2YDFtQA4h5GA_-c5DNesi58v_xS0DIMBtYBj2Gt53gCtTrtAq3j1F__5c2GX54aX_CMYwBZO9s4Zsw-dOshAET2iRTpfBK6iXg4Oan59Y9xNMf6uT2rrwT38A"})
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