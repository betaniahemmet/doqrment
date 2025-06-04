import io

from fpdf import FPDF
from PIL import Image


def generate_pdf_report(title: str, image_buffers: list[io.BytesIO]) -> io.BytesIO:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, title, ln=True, align="C")

    for i, buffer in enumerate(image_buffers):
        buffer.seek(0)
        img = Image.open(buffer)

        # Save to temporary file in memory in JPG format for FPDF
        temp_img = io.BytesIO()
        img.convert("RGB").save(temp_img, format="JPEG")
        temp_img.seek(0)

        img_path = f"temp_img_{i}.jpg"
        with open(img_path, "wb") as f:
            f.write(temp_img.read())

        # Insert image and add spacing
        pdf.image(img_path, x=10, y=None, w=pdf.w - 20)
        pdf.ln(10)

        # Clean up temp image file
        try:
            import os

            os.remove(img_path)
        except Exception:
            pass

    # Output to BytesIO
    output = io.BytesIO()
    pdf_output = pdf.output(dest="S").encode("latin1")
    output.write(pdf_output)
    output.seek(0)

    return output
