from flask import request, jsonify, abort

from backend.flaskr.utils import paginate
from backend.flaskr.models.models import Category


def categories(app):
    """
    All categorizes endpoint
    """

    @app.route("/categories", methods=["GET"])
    def all_categories():
        categories = Category.query.all()
        if not categories:
            abort(404, "No categories found")
        return jsonify({
            "success": True,
            "categories": {category.format()["id"]: category.format()["type"] for category in
                           paginate(request, categories)}
        })

    @app.route('/categories/<int:id_category>/questions', methods=['GET'])
    def get_questions_by_category(id_category: int):
        category = Category.query.get(id_category)
        if category is None:
            abort(404, 'There are no categories with this id in the database')
        return jsonify({
            "success": True,
            "questions": [question.format() for question in category.questions],
            "totalQuestions": len(category.questions),
            'currentCategory': category.type
        })
