from flask import request, jsonify, abort

from backend.flaskr.config import QUESTIONS_PER_PAGE
from backend.flaskr.models.models import Category


def categories(app):
    """
    All categorizes endpoint
    """

    @app.route("/categories", methods=["GET"])
    def all_categories():
        categories = Category.query.all()
        start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return jsonify({
            "success": True,
            "categories": {category.format()["id"]: category.format()["type"] for category in categories[start:end]}
        })

    @app.route('/categories/<int:id_category>/questions', methods=['GET'])
    def get_questions_by_category(id_category: int):
        category = Category.query.get(id_category)
        if category is None:
            abort(404)
        return jsonify({
            "success": True,
            "questions": [question.format() for question in category.questions],
            "totalQuestions": len(category.questions),
            'currentCategory': category.type
        })
