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


def generate_heatmap(values, timestamps, title="", save_path=None):
    buffer = io.BytesIO()
    df = pd.DataFrame({"value": values, "timestamp": timestamps})
    df["weekday"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour
    pivot = df.pivot_table(
        index="weekday", columns="hour", values="value", aggfunc="mean"
    )
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    pivot = pivot.reindex(weekday_order)

    plt.figure(figsize=(10, 5))
    sns.heatmap(
        pivot, cmap="coolwarm", center=df["value"].mean(), annot=True, fmt=".1f"
    )
    plt.title(title)
    plt.ylabel("Weekday")
    plt.xlabel("Hour of day")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer if not save_path else None


def generate_comparison_boxplot(
    values_a, label_a, values_b, label_b, focus, save_path=None
):
    buffer = io.BytesIO()
    df = pd.DataFrame(
        {
            "value": values_a + values_b,
            "session": [label_a] * len(values_a) + [label_b] * len(values_b),
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
