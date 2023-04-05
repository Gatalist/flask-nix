import os


class Config(object):
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 5000

    db_uri: str = 'postgresql'
    db_user: str = 'user_db'
    db_pass: str = 'xEhs5hU26nDNdeC'
    db_name: str = 'nix_db' # container_name to docker

    # TESTING = False
    # CSRF_ENABLED = True

    SECRET_KEY = '$%UHGD#O%$^htrfgolk546-fd[ssk;435gf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@localhost/{db_name}'

    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = os.path.join(ROOT_PATH, 'static')
    TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
    MEDIA_PATH = os.path.join(STATIC_PATH, 'media')

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
