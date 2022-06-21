from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from currencies import calculate_dependence, calculate_values, create_text

fileName = 'canvas_image.pdf'
documentTitle = 'documentTitle'
title = 'All you need to know about currencies... '


def add_image(image_path, text_lines):
    pdf = canvas.Canvas(fileName, pagesize=A4)
    pdf.setTitle(documentTitle)
    pdf.drawCentredString(330, 730, title)
    pdf.line(30, 710, 550, 710)
    text = pdf.beginText(30, 670)
    for line in text_lines:
        text.textLine(line)
    pdf.drawText(text)
    pdf.drawImage(image_path, 30, 100, width=500, height=500)
    pdf.save()


def create_pdf(image_path, currency_1, currency_2):
    text_lines = []
    for currency in [currency_1, currency_2]:
        _, money = calculate_dependence(currency)
        mean, maximum, minimum = calculate_values(money)
        text_lines.append(create_text(currency, mean, maximum, minimum))
    add_image(image_path, text_lines)
