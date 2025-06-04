import os

import qrcode
from fpdf import FPDF

from app.config import Config


def generate_qr_pdf(
    tracking_id, initials, location, save_to_file=False, filename="instance/label.pdf"
):
    # Ensure the instance folder exists
    os.makedirs("instance", exist_ok=True)

    # Prepare QR code data
    base_url = Config.BASE_URL
    qr_data = (
        f"{base_url}/log?"
        f"tracking_id={tracking_id}&initials={initials}&location={location}"
    )

    # Create and save QR code temporarily
    temp_path = os.path.join("instance", "qr_temp.png")
    try:
        qr = qrcode.make(qr_data)
        qr.save(temp_path)

        # Generate PDF
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Positioning
        qr_x, qr_y, qr_w = 60, 40, 90
        text_y = 140

        # Add QR image
        pdf.image(temp_path, x=qr_x, y=qr_y, w=qr_w)

        # Add text
        pdf.set_y(text_y)
        pdf.cell(0, 10, f"Tracking for: {initials} at {location}", ln=True, align="C")
        pdf.set_font("Arial", size=10)
        pdf.cell(
            0, 10, "Discard this QR if information is outdated", ln=True, align="C"
        )

        # Output PDF
        output = pdf.output(dest="S")
        if save_to_file:
            pdf.output(name=filename)
            return None
        return output.encode("latin1") if isinstance(output, str) else bytes(output)

    except Exception as e:
        print(f"[QR PDF ERROR] Failed to generate PDF: {e}")
        raise

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
