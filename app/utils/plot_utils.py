import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generate_line_plot(values, title="", ylabel="", xlabel="Log index", save_path=None):
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 4))
    sns.lineplot(x=range(len(values)), y=values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer if not save_path else None


def generate_box_plot(values, title="", ylabel="", save_path=None):
    buffer = io.BytesIO()
    plt.figure(figsize=(4, 6))
    sns.boxplot(y=values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer if not save_path else None


def generate_event_chart_by_day_lines(logs):
    """Each line is one day. Y-axis = number of events per hour."""
    import io

    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.DataFrame(
        [{"timestamp": log.timestamp} for log in logs if log.timestamp is not None]
    )

    df["day"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour

    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))

    for day, group in df.groupby("day"):
        hourly = group["hour"].value_counts().sort_index()
        plt.plot(hourly.index, hourly.values, label=str(day))

    plt.title("Händelser per timme (varje dag som en linje)")
    plt.xlabel("Klockslag")
    plt.ylabel("Antal händelser")
    plt.legend(title="Datum", fontsize="small", loc="upper right")
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer


def generate_event_chart_by_weekday_avg(logs):
    """One line: average number of events per hour for each weekday."""
    import io

    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.DataFrame(
        [{"timestamp": log.timestamp} for log in logs if log.timestamp is not None]
    )

    df["weekday"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour

    pivot = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)
    ordered_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    pivot = pivot.reindex(ordered_days).dropna(how="all")

    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))

    for weekday in pivot.index:
        plt.plot(pivot.columns, pivot.loc[weekday], label=weekday)

    plt.title("Genomsnittliga händelser per timme (per veckodag)")
    plt.xlabel("Klockslag")
    plt.ylabel("Antal händelser")
    plt.legend(title="Veckodag", fontsize="small")
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer


def generate_comparison_boxplot(
    values_a,
    label_a,
    values_b,
    label_b,
    focus,
    date_a=None,
    date_b=None,
    save_path=None,
):
    buffer = io.BytesIO()

    # Build improved labels with date ranges
    def format_label(label, date_range):
        return f"{label}\n{date_range}"

    label_a_full = format_label(label_a, date_a) if date_a else label_a
    label_b_full = format_label(label_b, date_b) if date_b else label_b

    # Ensure parent (label_b) comes first
    df = pd.DataFrame(
        {
            "value": values_b + values_a,
            "session": [label_b_full] * len(values_b) + [label_a_full] * len(values_a),
        }
    )

    plt.figure(figsize=(6, 6))
    sns.boxplot(x="session", y="value", data=df)
    plt.title(f"Comparison - {focus}")
    plt.ylabel(focus)
    plt.xlabel("Session")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer if not save_path else None
