import os


class Config(object):
    DEBUG: bool = True
    # HOST: str = "127.0.0.1"
    # HOST: str = "192.168.1.180"
    HOST: str = "0.0.0.0"
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
    PAGINATE_ITEM_IN_PAGE: int = 10


    # URLs
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Включает регистрацию
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = "/register/"
    SECURITY_SEND_REGISTER_EMAIL = False

    # Включет сброс пароля
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = "/reset/"
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True

    # Включает изменение пароля
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = "/change/"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    

    # ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    # MAX_CONTENT_LENGTH = 2000 * 1024  # 1 mb


    SECURITY_PASSWORD_SALT = 'nix-solt'
    SECURITY_PASSWORD_HASH = 'bcrypt'


# class ProdConfig(Config):
#     DEBUG = False


# class DevConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True
