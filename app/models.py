from datetime import datetime, timezone

from app import db


class MoodLog(db.Model):
    __tablename__ = "mood_logs"

    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    activities = db.Column(db.String, nullable=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<MoodLog {self.id}>"
