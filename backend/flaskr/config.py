from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

app = Flask(__name__)


def setup_db(app, database_path):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    return SQLAlchemy(app)


database_name = 'trivia'
database_path = f'postgresql://machk:machkour@localhost:5432/{database_name}'
moment = Moment(app)
db = setup_db(app, database_path)
migrate = Migrate(app, db)
