import random
import uuid
from datetime import datetime, timedelta

from app import create_app, db
from app.models import TrackingLog, TrackingSession


def run():
    app = create_app()
    app.app_context().push()

    initials = "AB"
    location = "Verkstan"
    focus = "Energinivå"
    activities_list = ["Promenad", "Bordtennis", "Samtal", "Skapande", "Fika", "Läsa"]

    print("🧪 Generating exportable dummy session...")

    # Create session that started 7 days ago
    created_at = datetime.now() - timedelta(days=9)
    tracking_id = str(uuid.uuid4())

    session = TrackingSession(
        id=str(uuid.uuid4()),
        tracking_id=tracking_id,
        parent_id=None,
        focus=focus,
        min_label="Trött",
        max_label="Pigg",
        duration="week",
        admin_email="test@betaniahemmet.se",
        initials=initials,
        location=location,
        tracking_mode="scale",
        activity_1="Promenad",
        activity_2="Bordtennis",
        activity_3="Samtal",
        activity_4="Skapande",
        created_at=created_at,
        exported=False,
    )
    db.session.add(session)
    db.session.flush()

    # Add logs from day 0 through day 7
    for day in range(8):  # include the final day
        ts = created_at + timedelta(days=day, hours=random.randint(8, 20))
        value = random.randint(3, 10)
        selected_acts = random.sample(activities_list, k=random.randint(1, 2))
        log = TrackingLog(
            timestamp=ts,
            value=value,
            activities=",".join(selected_acts),
            session_id=session.id,
        )
        db.session.add(log)

    # Create parent session to allow comparison
    parent_created_at = created_at - timedelta(days=21)
    parent_tracking_id = str(uuid.uuid4())

    parent_session = TrackingSession(
        id=str(uuid.uuid4()),
        tracking_id=parent_tracking_id,
        parent_id=None,
        focus=focus,
        min_label="Trött",
        max_label="Pigg",
        duration="week",
        admin_email="test@betaniahemmet.se",
        initials=initials,
        location=location,
        tracking_mode="scale",
        activity_1="Promenad",
        activity_2="Bordtennis",
        activity_3="Samtal",
        activity_4="Skapande",
        created_at=parent_created_at,
        exported=True,
    )
    db.session.add(parent_session)
    db.session.flush()

    # Link child to parent
    session.parent_id = parent_session.tracking_id

    for day in range(8):
        ts = parent_created_at + timedelta(days=day, hours=random.randint(8, 20))
        value = random.randint(1, 5)
        selected_acts = random.sample(activities_list, k=random.randint(1, 2))
        log = TrackingLog(
            timestamp=ts,
            value=value,
            activities=",".join(selected_acts),
            session_id=parent_session.id,
        )
        db.session.add(log)

    db.session.commit()
    print("✅ 1 exportable session created.")


if __name__ == "__main__":
    run()
