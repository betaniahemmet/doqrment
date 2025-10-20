import io

import qrcode
from fpdf import FPDF

from app.config import Config


def generate_qr_pdf(
    tracking_id: str,
    initials: str,
    location: str,
    filename: str = "instance/label.pdf",
    save_to_file: bool = False,
):
    """Generate a QR code label PDF (fpdf2, in-memory, type-clean)."""

    base_url = Config.BASE_URL or "http://localhost:5000"
    if not Config.BASE_URL:
        print("⚠️  BASE_URL missing — using http://localhost:5000")

    qr_data = f"{base_url}/log?tracking_id={tracking_id}&initials={initials}&location={location}"
    print(f"🧾 Generating QR for: {qr_data}")

    try:
        # Create QR image directly into memory
        qr_img = qrcode.make(qr_data)
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, "PNG")  # ✅ correct form
        qr_buffer.seek(0)

        # Build PDF
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        qr_x, qr_y, qr_w = 60, 40, 90
        text_y = 140

        # ✅ Insert in-memory image
        pdf.image(qr_buffer, x=qr_x, y=qr_y, w=qr_w)

        pdf.set_y(text_y)
        pdf.cell(0, 10, f"Tracking for: {initials} at {location}", ln=True, align="C")
        pdf.set_font("Helvetica", size=10)
        pdf.cell(
            0, 10, "Discard this QR if information is outdated", ln=True, align="C"
        )

        # ✅ output(dest="S") returns a bytearray — no encode() needed
        raw_bytes = pdf.output(dest="S")
        pdf_bytes = io.BytesIO(bytes(raw_bytes))
        pdf_bytes.seek(0)

        if save_to_file:
            pdf.output(filename)
            print(f"✅ PDF saved to: {filename}")
            return None

        return pdf_bytes

    except Exception as e:
        print(f"[QR PDF ERROR] Failed to generate PDF: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Running standalone QR PDF test...")
    pdf = generate_qr_pdf("test123", "AB", "Verkstan", save_to_file=True)
    print("✅ Done! Check instance/label.pdf")
