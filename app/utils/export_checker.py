from sqlalchemy import func

from app import db
from app.models import TrackingSession


def get_sessions_ready_for_export():
    now = func.now()

    week_sessions = db.session.query(TrackingSession).filter(
        TrackingSession.duration == "week",
        TrackingSession.exported.is_(False),
        TrackingSession.created_at <= func.datetime(now, "-7 days"),
    )

    month_sessions = db.session.query(TrackingSession).filter(
        TrackingSession.duration == "month",
        TrackingSession.exported.is_(False),
        TrackingSession.created_at <= func.datetime(now, "-30 days"),
    )

    eligible_sessions = week_sessions.union_all(month_sessions).all()

    results = []

    for session in eligible_sessions:
        # Find if this session is a parent (has follow-up sessions)
        has_children = (
            TrackingSession.query.filter_by(parent_id=session.tracking_id).first()
            is not None
        )

        # Find if this session is a child (follow-up)
        is_child = session.parent_id is not None

        # Only include standalone sessions or follow-up sessions (skip parent sessions unless isolated)
        if is_child or not has_children:
            results.append(session)

    print(f"Found {len(results)} sessions ready for export:")
    for s in results:
        print(f" - {s.tracking_id} ({s.created_at.date()}, exported={s.exported})")

    return results
