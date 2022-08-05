from flask import Flask
from flask_cors import CORS

from backend.flaskr.config import setup_db, db
from backend.flaskr.controllers.categories import categories
from backend.flaskr.controllers.questions import questions
from backend.flaskr.controllers.quiz import quiz

from backend.flaskr.errors.errors import error
from backend.flaskr.models.models import Category, Question




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, with_migrations=True)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    categories(app)

    questions(app)
    quiz(app)
    error(app)
    return app
