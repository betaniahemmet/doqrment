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
    generate_event_chart_by_day_lines,
    generate_event_chart_by_weekday_avg,
    generate_line_plot,
)

MIN_EVENTS = 10

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
        TrackingLog.query.filter_by(session_id=session.id)
        .order_by(TrackingLog.timestamp)
        .all()
    )

    values = [log.value for log in logs if log.value is not None]
    attachments = []

    # 📈 Scalar plots
    if session.tracking_mode == "scale" and values:
        attachments.append(
            generate_line_plot(values, title="Linjediagram", ylabel=session.focus)
        )
        attachments.append(
            generate_box_plot(values, title="Boxplot", ylabel=session.focus)
        )

    # 📊 Event-based visualizations
    if session.tracking_mode == "event" and len(logs) >= MIN_EVENTS:
        if session.duration == "week":
            attachments.append(
                generate_event_chart_by_day_lines(logs, start_date=session.created_at)
            )
        elif session.duration == "month":
            attachments.append(generate_event_chart_by_weekday_avg(logs))

    # 📤 Comparison if linked
    if session.parent_id:
        parent = TrackingSession.query.filter_by(tracking_id=session.parent_id).first()
        if parent:
            parent_logs = TrackingLog.query.filter_by(session_id=parent.id).all()
            parent_values = [log.value for log in parent_logs if log.value is not None]

            if parent_values:

                def get_date_range(logs):
                    timestamps = [log.timestamp for log in logs if log.timestamp]
                    return (
                        f"{min(timestamps).date()}-{max(timestamps).date()}"
                        if timestamps
                        else ""
                    )

                attachments.append(
                    generate_comparison_boxplot(
                        values_a=values,
                        label_a=session.initials,
                        date_a=get_date_range(logs),
                        values_b=parent_values,
                        label_b=parent.initials,
                        date_b=get_date_range(parent_logs),
                        focus=session.focus,
                    )
                )

    # 🖼 Save generated plots locally for inspection
    for i, buf in enumerate(attachments):
        with open(f"exported_plot_{i+1}.png", "wb") as f:
            f.write(buf.getbuffer())
    print("📂 Plots saved locally.")

    # 📧 Send the email
    try:
        body = (
            f"Hej, Här kommer en rapport för '{session.focus}' för "
            f"{session.initials} ({session.location}).\n"
            f"Vänliga hälsningar - Mätappens robot"
        )
        send_email_with_attachments(
            session.admin_email, "Din rapport är klar", body, attachments
        )
    except Exception as e:
        print(f"❌ Failed to export {session.tracking_id}: {e}")
        traceback.print_exc()
        return  # Abort without marking exported

    # ✅ Mark as exported
    session.exported = True
    db.session.commit()
    print(f"✔ Exported and emailed: {session.tracking_id}")


def run():
    sessions = get_sessions_ready_for_export()
    if not sessions:
        print("No sessions ready for export.")
        return

    for session in sessions:
        export_session(session)


if __name__ == "__main__":
    run()
