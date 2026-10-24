from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import random
import textwrap

def generate_certificate_pdf(name, issued_to, description, qr_code_bytes):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50
    content_width = width - 2 * margin

    # Border
    c.setLineWidth(4)
    c.setStrokeColor(colors.darkblue)
    c.roundRect(margin, margin, content_width, height - 2 * margin, 20, stroke=1, fill=0)

    # Organization Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 70, "Global Refugee Support Organization")

    # Collaboration Note
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 95, "In partnership with the United Humanitarian Alliance")

    # Motto
    c.setFont("Helvetica-Oblique", 12)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, height - 115, "\"Empowering displaced lives through opportunity and dignity.\"")

    # Certificate Title
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.darkred)
    c.drawCentredString(width / 2, height - 160, "Certificate of Recognition")

    # Presented To
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 195, "This is proudly awarded to")

    # Recipient Name
    c.setFont("Helvetica-BoldOblique", 22)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 225, issued_to)

    # Humanitarian Description
    wrapped_description = (
        f"In recognition of {issued_to}'s exceptional commitment, resilience, and dedication in successfully "
        f"completing the following humanitarian program:\n\n"
        f"“{description}”\n\n"
        f"This certificate honors their perseverance, effort, and pursuit of personal and community advancement "
        f"despite facing challenging circumstances as a displaced individual.\n\n"
        f"The Global Refugee Support Organization expresses its heartfelt appreciation for the recipient’s role "
        f"in uplifting themselves and those around them. Through this achievement, they serve as an inspiration "
        f"and beacon of hope for refugee communities around the world.\n\n"
        f"We commend their active engagement, commitment to learning, and contribution to building a more compassionate "
        f"and inclusive global society."
    )

    # Wrap and position the text
    lines = []
    for paragraph in wrapped_description.split("\n\n"):
        wrapped = textwrap.wrap(paragraph, width=90)
        lines.extend(wrapped + [""])

    text = c.beginText(margin + 20, height - 280)
    text.setFont("Helvetica", 12)
    text.setLeading(18)
    for line in lines:
        text.textLine(line)
    c.drawText(text)

    # Footer Info
    cert_id = f"GRSO-{random.randint(1000,9999)}-{datetime.now().strftime('%Y%m%d')}"
    footer_y = margin + 65
    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, footer_y, f"Certificate ID: {cert_id}")
    c.drawString(margin + 10, footer_y - 15, f"Issued By: {name}")
    c.drawString(margin + 10, footer_y - 30, f"Issued On: {datetime.now().strftime('%B %d, %Y')}")

    # Signature line
    c.line(width - 200, footer_y, width - 60, footer_y)
    c.setFont("Helvetica", 12)
    c.drawString(width - 190, footer_y - 15, "Authorized Signature")

    # QR Code
    if qr_code_bytes:
        qr_image = ImageReader(BytesIO(qr_code_bytes))
        c.drawImage(qr_image, width - 85, margin + 10, width=60, height=60)

    # Verification Note
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, margin + 10, "Verify this certificate at www.refugeesupport.org/verify")

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
