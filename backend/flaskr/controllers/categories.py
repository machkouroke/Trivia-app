from flask import request, jsonify

from backend.flaskr.config import QUESTIONS_PER_PAGE
from backend.flaskr.models.models import Category


def categories(app):
    """
    All categorizes endpoint
    """
    @app.route("/api/categories", methods=["GET"])
    def all_categories():
        categories = Category.query.all()
        start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return jsonify({
            "success": True,
            "categories": {category.format()["id"]: category.format()["type"] for category in categories[start:end]}
        })
