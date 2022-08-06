import logging

from flask import abort, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from backend.flaskr import db
from backend.flaskr.models.models import Category, Question
from backend.flaskr.config import setup_logging
from backend.flaskr.utils import paginate


def questions(app):
    """
    All questions endpoint
    """

    @app.route("/questions", methods=["GET"])
    def all_questions():
        questions = Question.query.all()

        # Error handling
        if not questions:
            abort(404, "No questions found")

        return jsonify({
            "success": True,
            "totalQuestions": len(questions),
            "questions": [question.format() for question in paginate(request, questions)],
            "categories": {category.format()["id"]: category.format()["type"] for category in Category.query.all()},
            "currentCategory": None
        })

    @app.route("/questions/<int:id_question>", methods=["DELETE"])
    def delete_questions(id_question: int):
        error: tuple[bool, None | int, str] = (False, None, "")
        try:
            db.session.delete(Question.query.get(id_question))
            db.session.commit()
        # Appears when the question does not exist
        except UnmappedInstanceError:
            db.session.rollback()
            error = (True, 404, "There is no question with this id")
        except Exception as e:
            setup_logging().debug(f"{type(e)}:{e}")
            error = (True, 500, "Internal Server error")
        finally:
            db.session.close()
            if error[0]:
                abort(error[1], error[2])

        return jsonify({
            "success": True,
            "message": f"Question with id:{id_question} is deleted"
        })

    @app.route('/questions', methods=['POST'])
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
            setup_logging().debug(f"{type(e)}:{e}")
            error = (True, 500)
        finally:
            db.session.close()
            if error[0]:
                abort(error[1])

        return jsonify({
            "success": True,
            "message": "Question added successfully"
        })

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        request_data = request.get_json()
        if 'searchTerm' not in request_data:
            abort(400)

        search_term = request_data['searchTerm']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "totalQuestions": len(questions),
            'currentCategory': None
        })
