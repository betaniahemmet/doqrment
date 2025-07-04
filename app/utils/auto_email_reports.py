from app import create_app, db
from app.utils.email_utils import send_email_with_attachments
from app.utils.export_checker import get_sessions_ready_for_export
from app.utils.report_utils import generate_report_for_session

app = create_app()
app.app_context().push()


def export_session(session):
    plots = generate_report_for_session(session)
    if not plots:
        return

    # Save locally
    for i, buf in enumerate(plots):
        with open(f"exported_plot_{i+1}.png", "wb") as f:
            f.write(buf.getbuffer())

    print("📂 Plots saved locally.")

    try:
        body = (
            f"Hej, Här kommer en rapport för '{session.focus}' för "
            f"{session.initials} ({session.location}).\n"
            f"Vänliga hälsningar - Mätappens robot"
        )
        send_email_with_attachments(
            session.admin_email, "Din rapport är klar", body, plots
        )
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return

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
