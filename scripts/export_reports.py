from datetime import datetime, timezone

from app import db
from app.models import TrackingLog, TrackingSession
from app.utils.pdf_report_generator import generate_pdf_report
from app.utils.plot_utils import create_activity_bar_chart, create_line_chart
from app.utils.save_report_to_folder import save_report_to_folder


def generate_and_export_all():
    sessions = TrackingSession.query.filter(
        TrackingSession.end_date <= datetime.now(timezone.utc),
        TrackingSession.exported.is_(False),
    ).all()

    for session in sessions:
        print(
            f"Exporting session {session.tracking_id} for {session.initials} at {session.location}..."
        )

        logs = (
            TrackingLog.query.filter_by(tracking_id=session.tracking_id)
            .order_by(TrackingLog.timestamp)
            .all()
        )

        if not logs:
            print("  No logs found. Skipping.")
            continue

        # Create charts
        chart_buffers = []

        scale_chart = create_line_chart(logs, session)
        chart_buffers.append(scale_chart)

        activity_chart = create_activity_bar_chart(logs, session)
        chart_buffers.append(activity_chart)

        # Generate PDF
        title = f"{session.focus} – {session.initials} @ {session.location}"
        pdf_bytes = generate_pdf_report(title, chart_buffers)

        # Save PDF
        save_report_to_folder(
            pdf_bytes,
            initials=session.initials,
            location=session.location,
            tracking_id=session.tracking_id,
        )

        # Mark as exported
        session.exported = True
        db.session.commit()

        print("  Export complete.")


if __name__ == "__main__":
    generate_and_export_all()
