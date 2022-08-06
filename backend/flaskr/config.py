from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from backend.settings import DB_NAME, DB_USER, DB_PASSWORD
import logging
from datetime import datetime

"""Db config"""

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


"""Logging config"""


def setup_logging() -> logging.Logger:
    """
    Setup logging configuration
    """
    logger = logging.getLogger(__name__)
    f_handler = logging.FileHandler(f'logging/{datetime.now().strftime("%Y-%m-%d")}.log')
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    return logger
