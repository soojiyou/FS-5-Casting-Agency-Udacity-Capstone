import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actors, Movies, db_drop_and_create_all, setup_db
import dateutil.parser
import babel
import json

from auth.auth import AuthError, requires_auth
# from config import app


# app = Flask(__name__)
# setup_db(app)
# CORS(app)
def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()

    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''@Todo endpoint get /actors and /movies
    /actors : get a list of actors
    /movies : get a list of movies

'''
    @app.route('/')
    def index():
        return redirect('dev-87bbhxlustzubkiq.us.auth0.com/authorize?response_type=token&client_id=dkQ2VMdKAjG46Rk7RcjEtfXTgX5L0fgl')

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actor')
    def get_actors(payload):
        actors_list = {}
        actors = Actors.query.all()
        if not actors:
            return abort(404)
        try:
            for actor in actors:
                actors_list[actor.id] = actor.name

            return jsonify({
                "success": True,
                "actors": actors_list,
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movie')
    def get_movies(payload):
        movies_list = {}
        movies = Movies.query.all()

        if not movies:
            return abort(404)
        try:
            for movie in movies:
                movies_list[movie.id] = movie.title

            return jsonify({
                "success": True,
                "movies": movies_list,
            }), 200
        except Exception:
            abort(422)

    '''@Todo endpoint get /actor and /movie
        /actors/<int:actor_id>' : get a detail of selected actor
        /movies/<int:movie_id> : get a detail of selected movie

    '''

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actor-detail')
    def get_actor_detail(payload, actor_id):
        try:
            actor_detail = Actors.query.get(actor_id)
            if not actor_detail:
                return abort(404)
            else:
                actor_data = actor_detail.format()

                return jsonify({
                    "success": True,
                    "actor_data": actor_data,
                }), 200
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movie-detail')
    def get_movie_detail(payload, movie_id):
        try:
            movie_detail = Movies.query.get(movie_id)
            if not movie_detail:
                return abort(404)
            else:
                movie_data = movie_detail.format()
                return jsonify({
                    "success": True,
                    "movie_data": movie_data,
                }), 200
        except Exception:
            abort(422)

    '''@Todo endpoint delete target /actor and /movie
        /actors/<int:actor_id>' : delete selected actor
        /movies/<int:movie_id> : delete selected movie

    '''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        target_actor = Actors.query.get(actor_id)
        if not target_actor:
            abort(404)

        try:
            target_actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id,
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        target_movie = Movies.query.get(movie_id)
        if not target_movie:
            abort(404)

        try:
            target_movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id,
            }), 200

        except Exception:
            abort(422)

    '''@Todo endpoint post new /actor and /movie
        /actors : post new actor
        /movies : post new movie

    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actors(payload):
        new_name = request.json.get('name')
        new_age = request.json.get('age')
        new_gender = request.json.get('gender')
        new_image = request.json.get('image_link')

        if not new_name and new_age and new_gender and new_image:
            abort(400)
        try:
            post_new_actor = Actors(
                name=new_name, age=new_age, gender=new_gender, image_link=new_image)
            post_new_actor.insert()

            actor_profile = post_new_actor.format()
            return jsonify({
                "success": True,
                "posted_actor_profile": actor_profile,
            }), 200
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movies(payload):
        new_title = request.json.get('title')
        new_release_date = request.json.get('release_date')
        new_genres = request.json.get('genres')
        new_image = request.json.get('image_link')

        if not new_title and new_release_date and new_genres and new_image:
            abort(400)
        try:
            post_new_movie = Movies(title=new_title, release_date=new_release_date,
                                    genres=new_genres, image_link=new_image)
            post_new_movie.insert()

            movie_profile = post_new_movie.format()
            return jsonify({
                "success": True,
                "posted_movie_profile": movie_profile,
            }), 200
        except:
            abort(422)

    '''@Todo endpoint patch requested /actor and /movie
        /actors/<int:actor_id> : patch requested actor
        /movies/<int:movie_id> : patch requested movie

    '''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actors(pqyload, actor_id):
        requested_actor = Actors.query.get(actor_id)
        if not requested_actor:
            abort(404)

        req_name = request.json.get('name')
        req_age = request.json.get('age')
        req_gender = request.json.get('gender')
        req_image = request.json.get('image_link')

        # if not req_name or not req_age or not req_gender or not req_image:
        #     abort(400)

        try:
            if req_name:
                requested_actor.name = req_name

            if req_age:
                requested_actor.age = req_age

            if req_gender:
                requested_actor.gender = req_gender

            if req_image:
                requested_actor.image_link = req_image

            requested_actor.update()

            patched_actor = requested_actor.format()
            return jsonify({
                'success': True,
                'patched_actor_profile': [patched_actor],
            }), 200

        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movies(pqyload, movie_id):
        requested_movie = Movies.query.get(movie_id)
        if not requested_movie:
            abort(404)

        req_title = request.json.get('title')
        req_release_date = request.json.get('release_date')
        req_genres = request.json.get('genres')
        req_image = request.json.get('image_link')

        # if not req_title or not req_release_date or not req_genres or not req_image:
        #     abort(400)

        try:
            if req_title:
                requested_movie.title = req_title

            if req_release_date:
                requested_movie.release_date = req_release_date

            if req_genres:
                requested_movie.genres = req_genres

            if req_image:
                requested_movie.image_link = req_image

            requested_movie.update()

            patched_movie = requested_movie.format()
            return jsonify({
                'success': True,
                'patched_movie_profile': patched_movie,
            }), 200

        except Exception:
            abort(422)


# Error Handling


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "bad request"}), 400

    @app.errorhandler(401)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "authentication error"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
                    "error": 422,
                     "message": "unprocessable"}), 422
        )

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({"success": False,
                        "error": 500,
                        "message": "Internal Server Error"}), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


# def format_datetime(value, format='medium'):

#     if isinstance(value, str):
#         date = dateutil.parser.parse(value)
#     else:
#         date = value
#     return babel.dates.format_datetime(date, format, locale='en')


# APP.jinja_env.filters['datetime'] = format_datetime
