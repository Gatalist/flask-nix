import os


class Config(object):
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000

    db_uri = 'postgresql'
    db_user = 'user_db'
    db_pass = 'xEhs5hU26nDNdeC'
    db_name = 'nix_db' # container_name to docker

    # TESTING = False
    # CSRF_ENABLED = True

    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = '$%UHGD#O%$^htrfgolk546-fd[ssk;435gf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@localhost/{db_name}'
    STATIC_FOLDER = os.path.join(ROOT_PATH, 'static')
    TEMPLATES_FOLDER = os.path.join(ROOT_PATH, 'templates')

    # FOLDER_USER = os.path.join(STATIC_FOLDER, 'media', 'user')

    # ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    # MAX_CONTENT_LENGTH = 2000 * 1024  # 1 mb


    # number_items_page = 3
    # NUMBER_ITEMS_PAGE = 3

    # SECURITY_PASSWORD_SALT = 'flask-solt-security'
    # SECURITY_PASSWORD_HASH = 'bcrypt'


# class ProdConfig(Config):
#     DEBUG = False


# class DevConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True
