import os
import logging
from config import Config
from flask import Flask
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_restful import Api
from typing import cast
from typings.sql_alchemy import SQLAlchemy as SQLAlchemyStub

app = Flask(__name__)
app.config.from_object(Config)

# db:SQLAlchemyStub = cast(SQLAlchemyStub, SQLAlchemy)
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login = LoginManager()
document_db = MongoEngine()
api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    document_db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    api.init_app(app)

    # from app.api import blueprint as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

from app import models
