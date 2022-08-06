import logging
from random import choice

from flask import request, jsonify, abort

from backend.flaskr.models.models import Category, Question
from backend.flaskr.config import setup_logging


def quiz(app):
    """
    All quizzes endpoint
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            data: dict = request.get_json()
            category: Category = Category.query.filter_by(id=data['quiz_category']['id']).one_or_none()
            # Id == 0 means all categories
            if data['quiz_category']['id'] == 0:
                all_question_list: list = [x[0] for x in
                                           Question.query.with_entities(
                                            Question.id)]
            elif category is None:
                raise AttributeError
            # With .with_entities the ids are returned as a tuple (id, ) to
            # facilitate comparison with the data sent in the requests we will convert them to integer
            else:
                all_question_list: list = [x[0] for x in
                                           Question.query.filter_by(category=category.id).with_entities(
                                               Question.id)]

            new_question = list(set(all_question_list) - set(data['previous_questions']))
            questions = Question.query.get(choice(new_question)).format()
            return jsonify({
                "success": True,
                "question": questions
            })
        # The user request is not valid
        except (KeyError, AttributeError):
            abort(400)
        except Exception as e:
            setup_logging().debug(f"{type(e)}:{e}")
            return jsonify({
                "success": False,
                "question": ''
            })
