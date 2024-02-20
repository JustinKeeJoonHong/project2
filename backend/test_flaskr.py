import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("hong-gijun", "dudwn84625", "localhost:5432", self.database_name)

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['total_questions'],19)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data['current_category'], 'Art')

    def test_search(self):
        search_term = {"searchTerm" : "movie"}
        res = self.client().post('/search', json=search_term)
        data = json.loads(res.data)
        
        self.assertEqual(len(data["questions"]),1)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()