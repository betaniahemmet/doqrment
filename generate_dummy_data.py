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
    parent_tracking_id = None

    print("Generating dummy sessions and logs...")

    # Create 2 sessions, 7 days apart
    for i in range(2):
        tracking_id = str(uuid.uuid4())
        created_at = datetime.now() - timedelta(days=(14 - i * 7))

        session = TrackingSession(
            id=str(uuid.uuid4()),
            tracking_id=tracking_id,
            parent_id=parent_tracking_id,
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
        )
        db.session.add(session)
        db.session.flush()

        if i == 0:
            parent_tracking_id = tracking_id

        for _ in range(20):
            hours_offset = random.randint(0, 7 * 24)
            ts = created_at + timedelta(hours=hours_offset)
            value = random.randint(3, 9) if i == 0 else random.randint(5, 10)

            selected_acts = random.sample(activities_list, k=random.randint(1, 2))
            log = TrackingLog(
                timestamp=ts,
                value=value,
                activities=",".join(selected_acts),
                session_id=session.id,
            )
            db.session.add(log)

    db.session.commit()
    print("Dummy data created.")


if __name__ == "__main__":
    run()
