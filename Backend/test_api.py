from flask_app import app  # ✅ Import your Flask app
from models import db, QuizCategory

# ✅ Use application context
with app.app_context():
    categories = QuizCategory.query.all()
    print([cat.name for cat in categories])  # ✅ Print categories
