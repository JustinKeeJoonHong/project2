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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "hong-gijun", "dudwn84625", "localhost:5432", self.database_name)

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

    # def test_get_questions(self):
    #     res = self.client().get('/questions?page=2')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(len(data['questions']), 6)
    #     self.assertEqual(data['total_questions'],16)
        
    def test_get_questions_failure(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        
    # def test_delete_question_success(self):

    #     res = self.client().delete('/questions/5')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data["deleted_question_id"], 5)


    def test_delete_question_failure(self):

        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
       

    def test_create_question_failure(self):
        request_data = {
            "question": "create test",
            "answer": "test",
            "difficulty": 1,
            "category": 100
        }
        res = self.client().post('/questions', json=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "There is internal Server Error.")
        # self.assertEqual(data['question'], "create asd1test")

    # def test_create_question_success(self):
    #     request_data = {
    #         "question": "create test",
    #         "answer": "test",
    #         "difficulty": 1,
    #         "category": 5
    #     }
    #     res = self.client().post('/questions', json=request_data)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['question'], "create test")


    def test_get_questions_by_category_success(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], 'Art')
    
    def test_get_questions_by_category_failure(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad request. Please check your data.")



    def test_search(self):
        search_term = {"searchTerm": "movie"}
        res = self.client().post('/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(len(data["questions"]), 1)

    def test_quizz(self):
        request_data = {
            'previous_questions': [20, 21],
            'quiz_category': {'type': 'Science', 'id': '1'}
        }
        res = self.client().post('/quizzes', json=request_data)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['next_question_id'], 22)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
