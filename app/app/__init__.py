import sys, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.settings import Config



app = Flask(__name__)
app.config.from_object(Config)
# app.config.from_file('settings.py')

bcrypt = Bcrypt(app)

# life time session
app.permanent_session_lifetime = datetime.timedelta(days=10)

# add root path
sys.path.append(app.config.get('ROOT_PATH'))

# flask login
login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# test client for unit test
client = app.test_client()

# create instance DataBase
db = SQLAlchemy(app)

# class instance Migrate
migrate = Migrate(app, db, compare_type=True)


# from app.admin import admin_panel
from app.admin.routes import app_admin

from app.movies import movie
from app.users import users


# app.register_blueprint(app_admin, url_prefix="/admin")
app.register_blueprint(movie, url_prefix='/')
app.register_blueprint(users, url_prefix='/user')


@app.shell_context_processor
def make_shell_context():
    return {"app": app, "db": db}
