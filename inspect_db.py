from app import create_app
from app.models import TrackingLog, TrackingSession

app = create_app()
app.app_context().push()

sessions = TrackingSession.query.all()
print(f"📊 {len(sessions)} sessions found.")
for s in sessions:
    print(
        f"Session {s.tracking_id[:8]} | Skapad: {s.created_at.date()} | Exported: {s.exported} | Duration: {s.duration}"
    )

    logs = (
        TrackingLog.query.filter_by(session_id=s.id)
        .order_by(TrackingLog.timestamp)
        .all()
    )
    print(f" - {len(logs)} logs")
    if logs:
        print(f"   First log: {logs[0].timestamp}")
        print(f"   Last  log: {logs[-1].timestamp}")
