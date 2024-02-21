import os
from models import Question, Category
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import math

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    def get_categories():
        categories = Category.query.all()
        categories_dict = {
            str(category.id): category.type for category in categories}

        return jsonify({
            'categories': categories_dict
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=["GET"])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        print(math.ceil(len(questions)/10))
        if page > math.ceil(len(questions)/10):
            abort(400)

        categories = Category.query.all()
        categories_dict = {
            str(category.id): category.type for category in categories}

        formatted_questions = [question.format() for question in questions]

        current_category = None
        category_filter = request.args.get('category', None)
        if category_filter:
            current_category = Category.query.get(category_filter)
            formatted_questions = [
                question for question in formatted_questions if question['category'] == current_category.id]

        paginated_questions = formatted_questions[start:end]

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(formatted_questions),
            'current_category': current_category.format() if current_category else None,
            'categories': categories_dict
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.


    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:questions_id>", methods=["DELETE"])
    def delete_question(questions_id):
        if questions_id == -1:
            abort(404)
        question = Question.query.filter(
            Question.id == questions_id).one_or_none()

        if question is None:
            abort(404)
        try:
            question.delete()

            return jsonify({
                "success": True,
                "deleted_question_id": questions_id
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def create_question():
        data = request.get_json()

        question = data.get("question")
        answer = data.get("answer")

        if not question or not answer:
            abort(404)

        difficulty = data.get("difficulty")
        category = data.get("category")

        try:
            new_question = Question(
                question=question, answer=answer, difficulty=difficulty, category=category)
            new_question.insert()
            return jsonify({
                'success': True,
                'create_question_id': new_question.id,
                'question': question
            })
        except:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        current_category = data.get("category", None)

        if current_category:
            category_object = Category.query.get(current_category)
            current_category_name = category_object.type if category_object else "Unknown"
        else:
            current_category_name = "All Categories"

        search_term = data.get('searchTerm', None)

        search_term = data.get('searchTerm', None)
        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            search_questions_list = [question.format()
                                     for question in search_results]
        else:
            abort(400)

        questions = Question.query.all()

        return jsonify({
            "success": True,
            "questions": search_questions_list,
            "totalQuestions": len(questions),
            "currentCategory": current_category_name
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.


    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):

        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            select_category = Category.query.get(id)
            select_questions_query = Question.query.filter(
                Question.category == id)
            select_questions = [question.format()
                                for question in select_questions_query.all()]
            paginated_questions = select_questions[start:end]

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(select_questions),
                'current_category': str(select_category.type)
            })
        except Exception as e:
            print(e)
            abort(400)

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
    @app.route('/quizzes', methods=["POST"])
    def create_quiz():
        data = request.get_json()
        pre_question_num_list = data.get('previous_questions', [])
        current_category = data.get('quiz_category')

        if not current_category:
            abort(400)

        if (current_category['id'] == 0):

            questions = Question.query.all()

        else:
            questions = Question.query.filter_by(
                category=current_category['id']).all()

        if not questions:
            return jsonify({
                "success": False,
                "message": "there is no question in this category"
            })

        if pre_question_num_list:
            questions = [
                question for question in questions if question.id not in pre_question_num_list]

        if questions:
            next_question = random.choice(questions).format()
        else:
            next_question = None

        return jsonify({
            "success": True,
            "question": next_question,
            "next_question_id": next_question['id']
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request. Please check your data."
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "We can't found your data. Please check your data."
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not found"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "There is internal Server Error."
        }), 500

    return app
