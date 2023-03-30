from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
# from forms import *
from flask_migrate import Migrate
# from app import APP
from sqlalchemy import Column, String, Integer, create_engine
# from datetime import datetime
import os
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)

# # TODO: connect to a local postgresql database
# migrate = Migrate(app, db)

# # with app.app_context():
#     db.create_all()
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# db = SQLAlchemy(APP)
# migrate = Migrate(APP, db)


database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
# database_path = "postgres:///{}".format(database_name)
# database_path = os.environ['DATABASE_URL']
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_name))

db = SQLAlchemy()

'''
setup_db(app)
        binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie = Movies(
        title='movietest1',
        release_date='20230315',
        genres='sci-fi',

        image_link='https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2'
    )

    movie.insert()
    actor = Actors(
        name='actortest1',
        age='23',
        gender='female',
        image_link='https://www.bing.com/th?id=OIP.M9AsZ7Sm6Qq-LXpY92Tt2AHaEK&w=180&h=185&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2'
    )
    actor.insert()


class Movies(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # release_date = db.Column(db.DateTime, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)

    image_link = db.Column(db.String(500))

    def __init__(self, title, release_date, genres, image_link):
        self.title = title
        self.release_date = release_date
        self.genres = genres
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movie_obj = {'movie_id': self.id, 'movie_title': self.title,
                     'release_date': self.release_date, 'genres': self.genres, 'image_link': self.image_link}
        return movie_obj


class Actors(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    image_link = db.Column(db.String(500))

    def __init__(self, name, age, gender, image_link):
        self.name = name
        self.age = age
        self.gender = gender
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        actor_obj = {'actor_id': self.id, 'actor_name': self.name,
                     'actor_age': self.age, 'actor_gender': self.gender, 'image_link': self.image_link}
        return actor_obj
