import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'for-later-use'

    # sql alchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # tika server
    TIKA_SERVER_ENDPOINT = os.environ.get('TIKA_SERVER_ENDPOINT') or 'http://localhost:9998'
    
    # mongodb, document database
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'

    MONGODB_SETTINGS = {
        'db': 'grace',
        'host': MONGODB_URI
    }