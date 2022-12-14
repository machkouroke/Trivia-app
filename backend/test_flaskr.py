import unittest

from flask_sqlalchemy import SQLAlchemy
from backend.flaskr import create_app, Question, Category
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

    def test_400_for_get_all_categories(self):
        """
        When the specified page is out of range, this error is returned.
        """
        for i in {0, 100}:
            res = self.client().get(f'{API_CATEGORIES}?page={i}')
            data = res.get_json()
            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

    def test_get_all_questions(self):
        res = self.client().get(API_QUESTIONS)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_400_for_get_all_questions(self):
        """
        When the specified page is out of range, this error is returned.
        """
        for i in {0, 100}:
            res = self.client().get(f'{API_QUESTIONS}?page={i}')
            data = res.get_json()
            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

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
        self.assertTrue(data['message'])

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
        self.assertTrue(data['message'])

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
        self.assertTrue(data['message'])

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
        self.assertTrue(data['message'])

    def test_get_quiz_questions(self):
        res = self.client().post(API_QUIZZES, json={
            'quiz_category': {'type': "Sports", 'id': 6},
            'previous_questions': [12, 23, 16],
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_get_quiz_questions__full(self):
        """
        Checks if when all the questions of a given category are
        already full the api returns None For the questions
        """
        category_id = 6
        res = self.client().post(API_QUIZZES, json={
            'quiz_category': {'type': "Sports", 'id': category_id},
            'previous_questions': [x.id for x in Category.query.get(category_id).questions],
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['question'])

    def test_400_for_failed_get_quiz_questions(self):
        res = self.client().post(API_QUIZZES, json={
            'quiz_category': {'type': "Techiou", 'id': 1000},
            'previous_questions': [12, 23, 16],
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
