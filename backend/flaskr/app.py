from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from sqlalchemy.orm.exc import UnmappedInstanceError

from backend.flaskr.models import Question, Category
from backend.flaskr.config import app, db
from backend.flaskr.errors import errors

QUESTIONS_PER_PAGE = 10

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
"""
@TODO: Use the after_request decorator to set Access-Control-Allow
"""


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.route("/api/categories")
def all_categories():
    categories = Category.query.all()
    start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return jsonify({
        "categories": {category.format()["id"]: category.format()["type"] for category in categories[start:end]}
    })


@app.route("/api/questions")
def all_questions():
    questions = Question.query.all()
    start = (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return jsonify({
        "totalQuestions": len(questions),
        "questions": [question.format() for question in questions[start:end]],
        "categories": {category.format()["id"]: category.format()["type"] for category in Category.query.all()},
    })


@app.route("/api/questions/<int:id_question>/delete", methods=["DELETE"])
def delete_questions(id_question: int):
    error = False
    try:
        db.session.delete(Question.query.get(id_question))
        db.session.commit()
    # Appears when the question does not exist
    except UnmappedInstanceError:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
        if error:
            abort(404)

    return jsonify({
        "success": True,
        "message": f"Question with id:{id_question} is deleted"
    })


"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""

"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""

"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""

"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""

"""
@TODO:
Create error handlers for all expected errors
including 404 and 422.
"""

if __name__ == '__main__':
    app.run(debug=True)
