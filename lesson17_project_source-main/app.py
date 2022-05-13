# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')

@movie_ns.route('/')
class BooksView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            movies_found = Movie.query.filter(Movie.director_id == int(director_id),
                                              Movie.genre_id == int(genre_id)).all()
            if not movies_found:
                return f"Не найдено", 204
            else:
                return movies_schema.dump(movies_found), 200

        if director_id:
            movies_found = Movie.query.filter(Movie.director_id == int(director_id)).all()
            if not movies_found:
                return f"Не найдено", 204
            else:
                return movies_schema.dump(movies_found), 200

        if genre_id:
            movies_found = Movie.query.filter(Movie.genre_id == int(genre_id)).all()
            if not movies_found:
                return f"Не найдено", 204
            else:
                return movies_schema.dump(movies_found), 200


if __name__ == '__main__':
    app.run(debug=True)
