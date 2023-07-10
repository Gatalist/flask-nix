from flask import Blueprint


movie = Blueprint('app_movies', __name__, template_folder='templates', static_folder='static')


from .routes import view_movie, search_movies
