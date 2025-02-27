from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime

# Create a blueprint for modular routes
main_bp = Blueprint('main', __name__)

# Path to the SQLite database
DATABASE_PATH = 'mood_tracking.db'

# Root route for the homepage
@main_bp.route('/')
def home():
    return render_template('index.html')

# Route to serve the frontend
@main_bp.route('/log', methods=['GET'])
def log_page():
    # Assuming the React app is bundled into 'index.html' in templates
    return render_template('index.html')

# Route to handle logging data
@main_bp.route('/log', methods=['POST'])
def log_event():
    data = request.json
    timestamp = data.get('timestamp', datetime.now().isoformat())
    mood = data.get('mood', 50)  # Default mood to 50 if not provided
    activities = ','.join(data.get('activities', []))

    # Save to SQLite database
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Ensure the table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                mood INTEGER,
                activities TEXT
            )
        ''')

        # Insert the log into the database
        cursor.execute('''
            INSERT INTO mood_logs (timestamp, mood, activities)
            VALUES (?, ?, ?)
        ''', (timestamp, mood, activities))

        conn.commit()
        conn.close()

        return jsonify({'timestamp': timestamp}), 200
    except Exception as e:
        print(f"Error saving to database: {e}")
        return jsonify({'error': 'Failed to save log'}), 500
