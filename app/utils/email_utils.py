import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
