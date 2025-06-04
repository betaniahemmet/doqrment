import smtplib
import traceback
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app import create_app, db
from app.models import TrackingLog, TrackingSession
from app.utils.export_checker import get_sessions_ready_for_export
from app.utils.plot_utils import (
    generate_box_plot,
    generate_comparison_boxplot,
    generate_heatmap,
    generate_line_plot,
)

app = create_app()
app.app_context().push()


def send_email_with_attachments(to_email, subject, body, image_buffers):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = "rapport@dinsida.se"
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    for i, img_buffer in enumerate(image_buffers):
        image = MIMEImage(img_buffer.read(), name=f"plot_{i+1}.png")
        image.add_header("Content-ID", f"<image{i+1}>")
        msg.attach(image)

    with smtplib.SMTP("smtp.example.com", 587) as smtp:
        smtp.starttls()
        smtp.login("rapport@dinsida.se", "your_password")
        smtp.send_message(msg)


def export_session(session):
    logs = (
        TrackingLog.query.filter_by(tracking_id=session.tracking_id)
        .order_by(TrackingLog.timestamp)
        .all()
    )
    values = [log.value for log in logs if log.value is not None]

    if not values:
        print(f"Skipping {session.tracking_id} – no values.")
        return

    attachments = []

    # Line plot
    attachments.append(
        generate_line_plot(values, title="Linjediagram", ylabel=session.focus)
    )

    # Box plot
    attachments.append(generate_box_plot(values, title="Boxplot", ylabel=session.focus))

    # Heatmap
    timestamps = [log.timestamp for log in logs if log.value is not None]
    attachments.append(generate_heatmap(values, timestamps, title="Värmekarta"))

    # Comparison if linked
    if session.parent_id:
        parent = TrackingSession.query.filter_by(tracking_id=session.parent_id).first()
        if parent:
            parent_logs = TrackingLog.query.filter_by(
                tracking_id=parent.tracking_id
            ).all()
            parent_values = [log.value for log in parent_logs if log.value is not None]
            if parent_values:
                label_a = f"{session.initials} {session.created_at.date()}"
                label_b = f"{parent.initials} {parent.created_at.date()}"
                attachments.append(
                    generate_comparison_boxplot(
                        values, label_a, parent_values, label_b, focus=session.focus
                    )
                )

    # Compose and send email
    try:
        body = (
            f"Hej, Här kommer en rapport för '{session.focus}' för "
            f"{session.initials} ({session.location})."
            f"Vänliga hälsningar - Mätappens robot"
        )
        send_email_with_attachments(
            session.admin_email, "Din rapport är klar", body, attachments
        )

        session.exported = True
        db.session.commit()
        print(f"✔ Exported and emailed: {session.tracking_id}")

    except Exception as e:
        print(f"❌ Failed to export {session.tracking_id}: {e}")
        traceback.print_exc()


def run():
    sessions = get_sessions_ready_for_export()
    if not sessions:
        print("No sessions ready for export.")
        return

    for session in sessions:
        export_session(session)


if __name__ == "__main__":
    run()
