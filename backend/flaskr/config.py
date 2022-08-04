from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = 'trivia'
database_path = f'postgresql://machk:machkour@localhost:5432/{database_name}'
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)