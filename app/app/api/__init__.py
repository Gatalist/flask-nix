from flask_restful import Api
from app import app
from .swagger_doc import Apispec_docs
from .routes import MoviesAPI


api = Api(app)
docs = Apispec_docs(app)


api.add_resource(MoviesAPI, '/movies')

docs.register(MoviesAPI)
