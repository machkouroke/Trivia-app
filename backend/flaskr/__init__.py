import logging
from random import choice

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from backend.flaskr.config import setup_db, db
from backend.flaskr.errors import error
from backend.flaskr.models import Category, Question

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route("/api/categories", methods=["GET"])
    def all_categories():
        categories = Category.query.all()
        start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return jsonify({
            "success": True,
            "categories": {category.format()["id"]: category.format()["type"] for category in categories[start:end]}
        })

    @app.route("/api/questions", methods=["GET"])
    def all_questions():
        questions = Question.query.all()
        start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return jsonify({
            "success": True,
            "totalQuestions": len(questions),
            "questions": [question.format() for question in questions[start:end]],
            "categories": {category.format()["id"]: category.format()["type"] for category in Category.query.all()},
        })

    @app.route("/api/questions/<int:id_question>", methods=["DELETE"])
    def delete_questions(id_question: int):
        print("suis ma")
        error: tuple[bool, None | int] = (False, None)
        try:

            db.session.delete(Question.query.get(id_question))
            db.session.commit()
        # Appears when the question does not exist
        except UnmappedInstanceError:
            db.session.rollback()
            error = (True, 404)
        except Exception as e:

            logging.error(f'{type(e)}: {e}')
            error = (True, 500)
        finally:

            db.session.close()
            if error[0]:
                abort(404)

        return jsonify({
            "success": True,
            "message": f"Question with id:{id_question} is deleted"
        })

    @app.route('/api/questions', methods=['POST'])
    def create_question():
        error: tuple[bool, None | int] = (False, None)
        try:
            question = Question(
                question=request.get_json()['question'],
                answer=request.get_json()['answer'],
                category=request.get_json()['category'],
                difficulty=request.get_json()['difficulty']
            )
            question.insert()

        except IntegrityError:
            db.session.rollback()
            abort(422)
        except Exception as e:
            logging.error(f'{type(e)}: {e}')
            error = (True, 500)
        finally:
            db.session.close()
            if error[0]:
                abort(error[1])

        return jsonify({
            "success": True,
            "message": "Question added successfully"
        })

    @app.route('/api/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "totalQuestions": len(questions)
        })

    @app.route('/api/questions/<int:id_category>', methods=['GET'])
    def get_questions_by_category(id_category: int):
        questions = Category.query.get(id_category).question
        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "totalQuestions": len(questions)
        })

    @app.route('/api/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            data: dict = request.get_json()
            category: int = Category.query.filter_by(type=data['category']).first().id

            # With .with_entities the ids are returned as a tuple (id, ) to
            # facilitate comparison with the data sent in the requests we will convert them to integer
            all_question_list: list = [x[0] for x in
                                       Question.query.filter_by(category=category).with_entities(Question.id)]
            new_question = list(set(all_question_list) - set(data['questions']))
            return jsonify({
                "success": True,
                "question": Question.query.get(choice(new_question)).format()
            })
        except (KeyError, AttributeError):
            abort(400)
        except Exception as e:
            logging.error(f'{type(e)}: {e}')
            abort(500)

    error(app)
    return app


