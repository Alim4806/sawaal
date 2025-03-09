from flask import render_template, request, jsonify
from models import db, Question, QuizResult, QuizCategory  # ✅ Ensure all models are imported
import quiz_logic  
import html  # ✅ Import for decoding HTML entities

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/categories')
    def categories():
        return render_template('categories.html')

    @app.route('/quiz/<category>')
    def quiz(category):  
        """Render quiz page when a category is selected."""
        return render_template('quiz.html', category=category)

    @app.route('/api/categories', methods=['GET'])  # ✅ Added missing API route
    def get_categories():
        """Fetch all quiz categories."""
        categories = QuizCategory.query.all()
        if not categories:
            return jsonify({'error': 'No categories found'}), 404
        return jsonify({'categories': [{'id': cat.id, 'name': cat.name} for cat in categories]})

    @app.route('/api/quiz', methods=['GET'])
    def get_quiz():
        """Fetch quiz questions for a given category name."""
        category_name = request.args.get('category')  

        if not category_name:
            return jsonify({'error': 'Category is required'}), 400
        
        # ✅ Find category using case-insensitive filter and strip spaces
        category = QuizCategory.query.filter(QuizCategory.name.ilike(category_name.strip())).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        try:
            questions = quiz_logic.generate_questions(category.name)  
            if not questions:
                return jsonify({'error': 'No questions found for this category'}), 404

            # ✅ Decode HTML entities in questions
            for q in questions:
                q["text"] = html.unescape(q["text"])
                q["option_a"] = html.unescape(q["option_a"])
                q["option_b"] = html.unescape(q["option_b"])
                q["option_c"] = html.unescape(q["option_c"])
                q["option_d"] = html.unescape(q["option_d"])
                q["correct_answer"] = html.unescape(q["correct_answer"])

            return jsonify({'questions': questions})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/submit_quiz', methods=['POST'])
    def submit_quiz():
        """Handles quiz submission and calculates score."""
        data = request.get_json()
        if not data or 'answers' not in data:
            return jsonify({'error': 'Answers are required'}), 400

        answers = data['answers']
        correct_count = 0
        total_questions = len(answers)

        for question_id, selected_option in answers.items():
            question = Question.query.get(question_id)
            if question and question.correct_answer == selected_option:
                correct_count += 1

        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        quiz_result = QuizResult(score=score, total_questions=total_questions, correct_answers=correct_count)
        db.session.add(quiz_result)
        db.session.commit()

        return jsonify({'score': score, 'correct_answers': correct_count, 'total_questions': total_questions})

    @app.route('/result')
    def result():
        """Displays the quiz result page."""
        return render_template('result.html')

    @app.route('/replay_or_quit')
    def rq():
        """Displays replay or quit options."""
        return render_template('rq.html')
