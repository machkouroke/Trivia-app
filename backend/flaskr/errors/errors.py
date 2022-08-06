from flask import jsonify
from werkzeug.exceptions import NotFound


def error(app):
    """
    Error handling
    """

    @app.errorhandler(404)
    def not_found(error: NotFound):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found: {error.description}",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Data is Unprocessable (Hint: Check if the category exists)"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request (Hint: Check if the category exists or if the keys of the body are correct)",
            "error_name": f"{error}"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
