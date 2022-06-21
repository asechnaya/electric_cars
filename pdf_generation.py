from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from currencies import calculate_dependence, calculate_values, create_text

fileName = 'canvas_image.pdf'
documentTitle = 'documentTitle'
title = 'All you need to know about currencies... '


def add_image(image_path, textLines):
    pdf = canvas.Canvas(fileName, pagesize=letter)
    pdf.setTitle(documentTitle)
    pdf.drawCentredString(330, 730, title)
    pdf.line(30, 710, 550, 710)
    print(textLines)
    # text = pdf.beginText(30, 700)
    # for line in textLines:
    #     text.textLine(line)
    # pdf.drawText(text)
    pdf.drawImage(image_path, 30, 100, width=500, height=500)
    pdf.save()


def create_pdf(image_path, currency_1, currency_2):
    textLines = ''
    for currency in [currency_1, currency_2]:
        _, money = calculate_dependence(currency)
        mean, maximum, minimum = calculate_values(money)
        textLines.join(create_text(currency, mean, maximum, minimum))
    print(textLines)
    add_image(image_path, textLines)
