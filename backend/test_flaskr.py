import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr.app import app
from backend.flaskr.config import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f"postgres://localhost:5432/{self.database_name}"
        self.db = setup_db(self.app, self.database_path)
        self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()