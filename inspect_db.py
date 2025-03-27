from app import create_app
from app.models import MoodLog

app = create_app()

with app.app_context():
    logs = MoodLog.query.all()
    for log in logs:
        print(f"ID: {log.id}")
        print(f"Mood: {log.mood}")
        print(f"Activities: {log.activities}")
        print(f"Timestamp: {log.timestamp}")
        print("-" * 20)
