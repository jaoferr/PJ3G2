import os
import logging
from config import Config
from flask import Flask
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from typing import cast
from typings.sql_alchemy import SQLAlchemy as SQLAlchemyStub

app = Flask(__name__)
app.config.from_object(Config)

db:SQLAlchemyStub = cast(SQLAlchemyStub, SQLAlchemy)
migrate = Migrate(compare_type=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    