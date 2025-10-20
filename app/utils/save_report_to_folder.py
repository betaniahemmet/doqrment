import io
from datetime import datetime
from pathlib import Path


def save_report_to_folder(
    report_bytes: io.BytesIO,
    initials: str,
    location: str,
    tracking_id: str,
    base_dir: Path = Path("reports"),
) -> Path:
    """
    Save the PDF report to a structured local folder:
    reports/YYYY-MM-DD_initials_location_trackingID/report.pdf

    Returns the full path to the saved PDF.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    safe_location = location.replace(" ", "_").replace("/", "-")
    safe_initials = initials.replace(" ", "_").upper()

    folder = base_dir / f"{today}_{safe_initials}_{safe_location}_{tracking_id}"
    folder.mkdir(parents=True, exist_ok=True)

    output_path = folder / "report.pdf"
    with open(output_path, "wb") as f:
        f.write(report_bytes.read())

    return output_path
