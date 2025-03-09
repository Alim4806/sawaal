from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  # Only import db here, models will be used inside routes
from routes import init_routes  # Import routes

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sawaal.db'  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register routes
init_routes(app)

# Ensure database tables are created before first request
with app.app_context():
    db.create_all()

# Run the app only if executed directly
if __name__ == '__main__':
    app.run(debug=True)
