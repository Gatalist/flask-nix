from flask import jsonify
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource

from app.api.schemas import MoviesSchema
from app.api.auth import basic_auth
from app.movies.models import Movies
from app import db, logger



class MoviesAPI(MethodResource, Resource):
    @logger.catch
    @doc(description='My First GET Awesome API.', tags=['Movies'])
    @marshal_with(MoviesSchema)  # marshalling
    @basic_auth.login_required
    def get(self):
        movie = Movies.query.all()
        schema = MoviesSchema(many=True)
        return jsonify(schema.dump(movie))


    @logger.catch
    @doc(description='My First GET Awesome API.', tags=['Movies'])
    @use_kwargs(MoviesSchema, location=('json'))
    @marshal_with(MoviesSchema)  # marshalling
    @basic_auth.login_required
    def post(self, **kwargs):
        movie = Movies(**kwargs)
        db.session.add(movie)
        db.session.commit()
        movies = Movies.query.all()
        schema = MoviesSchema(many=True)
        return jsonify(schema.dump(movies))


    @logger.catch
    @doc(description='update movie', tags=['Movies'])
    @use_kwargs(MoviesSchema, location=('json'))
    @marshal_with(MoviesSchema)
    @basic_auth.login_required
    def update(self, **kwargs):
        movie = Movies(**kwargs)
        db.session.add(movie)
        db.session.commit()
        movies = Movies.query.all()
        schema = MoviesSchema(many=True)
        return jsonify(schema.dump(movies))


    @logger.catch
    @doc(description='delete movie', tags=['Movies'])
    @marshal_with(MoviesSchema)
    @basic_auth.login_required
    def delete(self, movie_id):
        movie = Movies.query.filter_by(id=movie_id).first()
        db.session.delete(movie)
        db.session.commit()
        movies = Movies.query.all()
        schema = MoviesSchema(many=True)
        return jsonify(schema.dump(movies))
