import base64
from io import BytesIO

import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_qr_data(url):
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('ascii')


def generate_certificate_pdf(participant):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    event_title = participant.event.title

    pdf.setTitle(f'Certificate - {participant.name}')
    pdf.setStrokeColor(colors.HexColor('#334155'))
    pdf.setLineWidth(2)
    pdf.roundRect(1.7 * cm, 1.7 * cm, width - 3.4 * cm, height - 3.4 * cm, 12, stroke=1, fill=0)
    pdf.setFillColor(colors.HexColor('#0f766e'))
    pdf.setFont('Helvetica-Bold', 28)
    pdf.drawCentredString(width / 2, height - 6 * cm, 'Certificate of Participation')
    pdf.setFillColor(colors.HexColor('#334155'))
    pdf.setFont('Helvetica', 14)
    pdf.drawCentredString(width / 2, height - 8 * cm, 'This certifies that')
    pdf.setFillColor(colors.black)
    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawCentredString(width / 2, height - 10 * cm, participant.name)
    pdf.setFont('Helvetica', 14)
    pdf.drawCentredString(width / 2, height - 12 * cm, f'has successfully completed {event_title}.')
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawCentredString(width / 2, height - 13.3 * cm, f'Marks: {participant.marks}/100')
    pdf.setFont('Helvetica-Oblique', 9)
    pdf.setFillColor(colors.HexColor('#64748b'))
    pdf.drawCentredString(width / 2, 3.1 * cm, f'Reference: {participant.certificate_hash}')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
