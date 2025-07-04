from app.models import TrackingLog, TrackingSession
from app.utils.plot_utils import (
    generate_box_plot,
    generate_comparison_boxplot,
    generate_event_chart_by_day_lines,
    generate_event_chart_by_weekday_avg,
    generate_line_plot,
)


def get_date_range(logs):
    timestamps = [log.timestamp for log in logs if log.timestamp]
    return f"{min(timestamps).date()}-{max(timestamps).date()}" if timestamps else ""


def generate_report_for_session(session):
    from app import db  # noqa: F401

    attachments = []

    logs = (
        TrackingLog.query.filter_by(session_id=session.id)
        .order_by(TrackingLog.timestamp)
        .all()
    )
    values = [log.value for log in logs if log.value is not None]

    if not values:
        print(f"Skipping {session.tracking_id} - no values.")
        return []

    # Line + Box
    attachments.append(
        generate_line_plot(values, title="Linjediagram", ylabel=session.focus)
    )
    attachments.append(generate_box_plot(values, title="Boxplot", ylabel=session.focus))

    # Event charts
    if session.tracking_mode == "event":
        if session.duration == "week":
            attachments.append(generate_event_chart_by_day_lines(logs))
        elif session.duration == "month":
            attachments.append(generate_event_chart_by_weekday_avg(logs))

    # Comparison
    if session.parent_id:
        parent = TrackingSession.query.filter_by(tracking_id=session.parent_id).first()
        if parent:
            parent_logs = TrackingLog.query.filter_by(session_id=parent.id).all()
            parent_values = [log.value for log in parent_logs if log.value is not None]
            if parent_values:
                label_parent = session.initials
                label_child = session.initials
                date_range_parent = get_date_range(parent_logs)
                date_range_child = get_date_range(logs)

                attachments.append(
                    generate_comparison_boxplot(
                        values_a=values,
                        label_a=label_child,
                        values_b=parent_values,
                        label_b=label_parent,
                        focus=session.focus,
                        date_a=date_range_child,
                        date_b=date_range_parent,
                    )
                )

    return attachments
