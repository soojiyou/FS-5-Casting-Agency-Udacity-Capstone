
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app, get_headers
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://postgres:abc@localhost:5432/capstone'
        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # self.db.db_drop_and_create_all()

        # test case input for movie

        self.test_movie_post1 = {
            "title": "movietest2",
            "release_date": "20230316",
            "genres": "sci-fi2",
            "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
        }
        self.test_movie_post2 = {}
        self.test_movie_patch1 = {"title": "movietest2-1"}
        self.test_movie_patch2 = {"name": "wrong param"}

        # test case input for actor
        self.test_actor_post1 = {
            "name": "actortest2",
            "age": "20",
            "gender": "male",
            "image_link": "https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2"
        }
        self.test_actor_post2 = {}
        self.test_actor_patch1 = {"name": "actortest1-2"}
        self.test_actor_patch2 = {"title": "wrong param"}

        self.unauthorized_jwt = 'sggegw'
        self.producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVvRzNSOXRzdkVOZDRtTmpmUUlMNCJ9.eyJpc3MiOiJodHRwczovL2Rldi04N2JiaHhsdXN0enVia2lxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDA0MGNiODExMTRhM2RhYjJmN2VkZTAiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTY3ODk1ODQ5NCwiZXhwIjoxNjc4OTk0NDk0LCJhenAiOiJka1EyVk1kS0FqRzQ2Ums3UmNqRXRmWFRnWDVMMGZnbCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0OmFjdG9yLWRldGFpbCIsImdldDptb3ZpZSIsImdldDptb3ZpZS1kZXRhaWwiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.RlmFt7XN0QXwmGX3PAoodZpkxYgQhiZweu1Q0LmNYRe9eU2C3cWnUjYEoa-kYEgW_5fvI2bGomv7GapSE36eorao9bfkitcw8sKv5DGbCC3C3KMlIoy_Zjhj-C07bBjGnKHL0v8Ys40m48x7SAXLLkgI_P_4BxaiOYmN1SE973gNMVOttFZYrVY-Z7aEIWFPjPTIpR5BqLGN6MF7W81GUL5dToLuxCoqWhDQIuIJJW0tAIv3soxkZFzg0ExZC89s-Aptst5IX6yCCB5RgZbOB1-_v_0XgCH5lynRZZR7D5sIXE9LBl0NrUc-PpePmTaKIVln7IW0HlXn4oSb2PKr7Q'

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_movie_list(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().get(
            '/movies',  headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        # movies = Movies.query.get(1)
        # movies_list = {}
        # movie_id = 1
        # movies = Movies.query.get(movie_id)
        # movies_list = movies.title

        movie = Movies.query.filter_by(id=1).first()
        title = movie.title
        # print(title)
        # print(data)

        # print(movies_list)
        # movie_title = movies.title
        # self.assertEqual(data["movies"]["1"])
        self.assertEqual(data["movies"]["1"], title)

    def test_get_movie_list_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        # db_drop_and_create_all()
        response = self.client().get(
            '/movies',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_get_actor_list(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().get(
            '/actors',  headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actors.query.get(1)
        actor_name = actors.name
        print(actor_name)
        self.assertEqual(data["actors"]["1"], actor_name)

    def test_get_actor_list_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().get(
            '/actors',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_get_movie_detail(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().get(
            '/movies/1',  headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        movies = Movies.query.get(1)
        movies_format = movies.format()
        self.assertEqual(data["movie_data"], movies_format)

    def test_get_movie_detail_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().get(
            '/movies/1',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_get_actor_detail(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().get(
            '/actors/1',  headers=auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actors.query.get(1)
        actors_format = actors.format()
        self.assertEqual(data["actor_data"], actors_format)

    def test_get_actor_detail_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().get(
            '/actors/1',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_delete_movie(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().delete(
            '/movies/1',  headers=auth_header)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

    def test_delete_actor(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().delete(
            '/actors/1',  headers=auth_header)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 1)

    def test_delete_movie_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().delete(
            '/movies/1',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_delete_actor_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().delete(
            '/actors/1',  headers=auth_header)
        self.assertEqual(response.status_code, 401)

    def test_post_movie(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().post(
            '/movies',  headers=auth_header, json=self.test_movie_post1)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('posted_movie_profile', data)

    def test_post_actor(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().post(
            '/actors',  headers=auth_header, json=self.test_actor_post1)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('posted_actor_profile', data)

    def test_post_movie_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().post(
            '/movies',  headers=auth_header, json=self.test_movie_post2)

        self.assertEqual(response.status_code, 401)

    def test_post_actor_err(self):
        auth_header = get_headers(self.unauthorized_jwt)
        response = self.client().post(
            '/actors',  headers=auth_header, json=self.test_actor_post2)

        self.assertEqual(response.status_code, 401)

    def test_update_movie(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().patch(
            '/movies/1',  headers=auth_header, json=self.test_movie_patch1)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        # self.assertIn('patched_movie_profile', data)

    def test_update_actor(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().patch(
            '/actors/1',  headers=auth_header, json=self.test_actor_patch1)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        # self.assertIn('patched_actor_profile', data)

    def test_update_movie_err(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().post(
            '/movies/1',  headers=auth_header, json=self.test_movie_patch2)

        self.assertEqual(response.status_code, 405)

    def test_update_actor_err(self):
        auth_header = get_headers(self.producer_jwt)
        response = self.client().post(
            '/actors/1',  headers=auth_header, json=self.test_actor_patch2)

        self.assertEqual(response.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
