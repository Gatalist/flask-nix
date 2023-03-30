import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


from .settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

app = create_app()

# test client for unit test
client = app.test_client()

# create instance DataBase
db = SQLAlchemy(app)

# class instance Migrate
migrate = Migrate(app, db)


from .models import Genres, Users, Movies, Directors, Ratings
from .admin import GenreView, UserView, MovieView, RatingView, DirectorView

# class instance Admin panel flask
admin = Admin(app)

admin.add_view(UserView(Users, db.session))
admin.add_view(GenreView(Genres, db.session))
admin.add_view(MovieView(Movies, db.session))
admin.add_view(RatingView(Ratings, db.session))
admin.add_view(DirectorView(Directors, db.session))



@app.route('/')
def hello():
    return 'Hello my dir friends'


@app.shell_context_processor
def make_shell_context():
    return {'db': db}
