import sys
from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.settings import Config


app = Flask(__name__)
app.config.from_object(Config)

# add root path
sys.path.append(app.config.get('ROOT_PATH'))

# test client for unit test
client = app.test_client()

# create instance DataBase
db = SQLAlchemy(app)

# class instance Migrate
migrate = Migrate(app, db)

# class instance Admin panel flask
admin_panel = Admin(app)


from app.movies.models import Genres, Movies, Ratings, Directors, Reliase
from app.users.models import Users
from app.admin import UserView, GenreView, MovieView, RatingView, DirectorView, ReliaseView

admin_panel.add_view(UserView(Users, db.session))
admin_panel.add_view(GenreView(Genres, db.session))
admin_panel.add_view(MovieView(Movies, db.session))
admin_panel.add_view(RatingView(Ratings, db.session))
admin_panel.add_view(DirectorView(Directors, db.session))
admin_panel.add_view(ReliaseView(Reliase, db.session))


from app.movies import movie
from app.users import users


app.register_blueprint(movie, url_prefix='/')
app.register_blueprint(users, url_prefix='/users')


@app.shell_context_processor
def make_shell_context():
    return {"app": app, "db": db}

