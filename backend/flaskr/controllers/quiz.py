import logging
from random import choice

from flask import request, jsonify, abort

from backend.flaskr.models.models import Category, Question


def quiz(app):
    """
    All quizzes endpoint
    """
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
