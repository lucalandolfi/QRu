import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY must be a 32byte, base64 encoded, URL safe string
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_TOKEN_AGE = os.environ.get('MAX_TOKEN_AGE') or 15
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass
