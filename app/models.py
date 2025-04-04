import uuid
from datetime import datetime

from app import db


class TrackingSession(db.Model):
    __tablename__ = "tracking_sessions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tracking_id = db.Column(db.String(36), nullable=False, unique=True)
    measurement_type = db.Column(db.String(100), nullable=False)
    min_label = db.Column(db.String(100), nullable=False)
    max_label = db.Column(db.String(100), nullable=False)
    activity_1 = db.Column(db.String(100), nullable=True)
    activity_2 = db.Column(db.String(100), nullable=True)
    activity_3 = db.Column(db.String(100), nullable=True)
    activity_4 = db.Column(db.String(100), nullable=True)
    activity_5 = db.Column(db.String(100), nullable=True)
    activity_6 = db.Column(db.String(100), nullable=True)
    activity_7 = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.String(10), nullable=False)  # "Week" or "Month"
    admin_email = db.Column(db.String(255), nullable=False)
    initials = db.Column(db.String(2), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship("TrackingLog", backref="session", lazy=True)


class TrackingLog(db.Model):
    __tablename__ = "tracking_logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Integer, nullable=False)
    activities = db.Column(db.String(500), nullable=True)

    session_id = db.Column(
        db.String(36), db.ForeignKey("tracking_sessions.id"), nullable=False
    )


def __repr__(self):
    return f"<TrackingLog {self.id} - Session {self.session_id}>"
