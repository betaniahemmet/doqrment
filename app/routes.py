from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request

from app import db
from app.models import MoodLog

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/log", methods=["GET"])
def log_page():
    return render_template("index.html")


@main_bp.route("/log", methods=["POST"])
def log_event():
    data = request.json
    timestamp = datetime.now(timezone.utc)
    mood = data.get("mood", 50)
    activities = ",".join(data.get("activities", []))

    try:
        new_log = MoodLog(mood=mood, activities=activities, timestamp=timestamp)
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"timestamp": timestamp.isoformat()}), 200
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to save log"}), 500
