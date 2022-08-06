from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from backend.settings import DB_NAME, DB_USER, DB_PASSWORD

database_name = DB_NAME
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{database_name}'
QUESTIONS_PER_PAGE = 10
db = SQLAlchemy()


def setup_db(app, database_path=database_path, with_migrations=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    if with_migrations:
        migrate = Migrate(app, db)
