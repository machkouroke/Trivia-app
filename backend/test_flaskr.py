import unittest

from flask_sqlalchemy import SQLAlchemy
from backend.flaskr import create_app, Question
from backend.flaskr.config import setup_db
from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD

API_QUIZZES = '/quizzes'
API_CATEGORIES = '/categories'
API_QUESTIONS = '/questions'


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()

            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get(API_CATEGORIES)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_all_questions(self):
        res = self.client().get(API_QUESTIONS)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_create_question(self):
        res = self.client().post(API_QUESTIONS, json={
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': '3',
            'difficulty': '1'
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['message'])

    def test_delete_questions(self):
        """
        Delete the last question inserted
        """
        id_question = Question.query.order_by(Question.id).all()[-1].id
        res = self.client().delete(f'{API_QUESTIONS}/{id_question}')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'Question with id:{id_question} is deleted')

    def test_404_for_failed_delete_questions(self):
        id_question = 100
        res = self.client().delete(f'{API_QUESTIONS}/{id_question}')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found (Hint: check your Url)')

    def test_422_for_failed_create_question(self):
        res = self.client().post(API_QUESTIONS, json={
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': '10',
            'difficulty': '1'
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Data is Unprocessable (Hint: Check if the category exists)')

    def test_search_question(self):
        res = self.client().post(f'{API_QUESTIONS}/search', json={
            'searchTerm': 'What'
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_400_for_search_question(self):
        res = self.client().post(f'{API_QUESTIONS}/search', json={
            'searchTer': ''
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Bad request (Hint: Check if the category exists or if the keys of the body are correct)')

    def test_get_questions_by_category(self):
        res = self.client().get(f'{API_CATEGORIES}/5/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_404_for_get_questions_by_category(self):
        res = self.client().get(f'{API_CATEGORIES}/100/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found (Hint: check your Url)')

    def test_get_quiz_questions(self):
        res = self.client().post(API_QUIZZES, json={
            'quiz_category': {'type': "Sports", 'id': 6},
            'previous_questions': [12, 23, 16],
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_400_for_failed_get_quiz_questions(self):
        res = self.client().post(API_QUIZZES, json={
            'quiz_category': {'type': "Techiou", 'id': 1000},
            'previous_questions': [12, 23, 16],
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Bad request (Hint: Check if the category exists or if the keys of the body are correct)')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
