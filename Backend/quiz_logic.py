import random
import requests
import html  # Import for decoding HTML entities
from models import db, Question, QuizCategory  # Import models correctly

# OpenTDB Category Mapping
CATEGORY_MAPPING = {
    "general": 9,          # General Knowledge
    "science": 17,         # Science & Nature
    "history": 23,         # History
    "math": 19,            # Mathematics
    "entertainment": 11,   # Entertainment (Film)
    "sports": 21           # Sports
}

def fetch_questions_from_api(category_name):
    """Fetch quiz questions from OpenTDB API."""
    opentdb_category_id = CATEGORY_MAPPING.get(category_name)
    if not opentdb_category_id:
        print(f"❌ Error: No valid category mapping found for '{category_name}'")
        return []

    api_url = f"https://opentdb.com/api.php?amount=10&category={opentdb_category_id}&type=multiple"
    print(f"🔹 Fetching questions from: {api_url}")

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        data = response.json()

        if data['response_code'] != 0:
            print(f"❌ API Error: {data['response_code']} (No questions returned)")
            return []

        questions = []
        for item in data.get('results', []):
            incorrect_answers = [html.unescape(ans) for ans in item['incorrect_answers']]
            correct_answer = html.unescape(item['correct_answer'])

            options = incorrect_answers + [correct_answer]
            random.shuffle(options)

            question = {
                'text': html.unescape(item['question']),
                'option_a': options[0],
                'option_b': options[1],
                'option_c': options[2],
                'option_d': options[3],
                'correct_answer': correct_answer
            }
            questions.append(question)

        print(f"✅ Successfully fetched {len(questions)} questions")
        return questions
    except requests.RequestException as e:
        print(f"❌ Error fetching questions: {e}")
        return []

def generate_questions(category_name):
    """Generates 10 quiz questions dynamically."""

    print(f"🔹 Looking for category: {category_name}")
    category = QuizCategory.query.filter_by(name=category_name).first()
    
    if not category:
        print(f"❌ Error: Category '{category_name}' not found in database!")
        return []

    print(f"✅ Found category '{category.name}' (ID: {category.id})")

    # Check if existing questions are available
    existing_questions = Question.query.filter_by(category_id=category.id).limit(10).all()
    if existing_questions:
        print(f"✅ Using existing questions from database for category '{category_name}'")
        return [
            {
                'text': q.text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer
            }
            for q in existing_questions
        ]

    print(f"🔹 Fetching new questions from API for category '{category_name}'...")
    questions = fetch_questions_from_api(category_name)

    if not questions:
        print(f"❌ No questions retrieved for category '{category_name}'")
        return []

    print(f"✅ Storing {len(questions)} new questions in the database...")
    for q in questions:
        question = Question(
            text=q['text'],
            option_a=q['option_a'],
            option_b=q['option_b'],
            option_c=q['option_c'],
            option_d=q['option_d'],
            correct_answer=q['correct_answer'],
            category_id=category.id
        )
        db.session.add(question)

    db.session.commit()
    print(f"✅ Questions saved successfully!")

    return questions
